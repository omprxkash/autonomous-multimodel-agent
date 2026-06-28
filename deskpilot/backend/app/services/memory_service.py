"""
MemoryService — graph-based memory with semantic + importance-based hybrid retrieval.
Uses pgvector for similarity search via SQLAlchemy ORM.
"""
import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import MemoryFact, MemoryEmbedding

logger = logging.getLogger("deskpilot")

_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)
_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


class MemoryNode:
    def __init__(self, fact: str, category: str, importance: float, metadata: Dict[str, Any] = None):
        self.id = str(uuid.uuid4())
        self.fact = fact
        self.category = category
        self.importance = importance
        self.metadata = metadata or {}
        self.connections: List[str] = []


class MemoryGraph:
    def __init__(self):
        self.nodes: Dict[str, MemoryNode] = {}

    def add(self, node: MemoryNode) -> MemoryNode:
        self.nodes[node.id] = node
        return node

    def connect(self, id1: str, id2: str):
        if id1 in self.nodes and id2 in self.nodes:
            self.nodes[id1].connections.append(id2)
            self.nodes[id2].connections.append(id1)

    def by_importance(self, min_importance: float = 0.0, category: str | None = None) -> List[MemoryNode]:
        return sorted(
            [n for n in self.nodes.values()
             if n.importance >= min_importance and (category is None or n.category == category)],
            key=lambda x: x.importance,
            reverse=True,
        )


class MemoryService:

    @staticmethod
    async def extract_facts(user_id: str, message: str, db: AsyncSession) -> List[MemoryNode]:
        """Use Gemini to extract structured facts from a message and store them."""
        prompt = f"""Analyse this message and extract important facts about the user.

Message: {message}

Return a JSON array of objects with:
- fact: concise specific information
- category: one of [preference, habit, project, relationship, constraint, event, personal]
- importance: 0.0 to 1.0
- metadata: dict of additional context

Return only valid JSON, no markdown. If nothing important, return [].

Examples:
- "I hate 9 AM meetings" → {{"fact": "User dislikes meetings before 10 AM", "category": "preference", "importance": 0.9, "metadata": {{}}}}
- "Project X is delayed" → {{"fact": "Project X has delays", "category": "project", "importance": 0.8, "metadata": {{}}}}"""

        try:
            response = await _llm.ainvoke([HumanMessage(content=prompt)])
            content = response.content
            if "```" in content:
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.split("```")[0]
            facts_data = json.loads(content.strip())
            if not isinstance(facts_data, list):
                return []

            nodes = []
            for fd in facts_data:
                fact_text = fd.get("fact", "").strip()
                if not fact_text:
                    continue
                node = MemoryNode(
                    fact=fact_text,
                    category=fd.get("category", "personal"),
                    importance=float(fd.get("importance", 0.5)),
                    metadata=fd.get("metadata", {}),
                )
                await MemoryService.store_fact(user_id, node.fact, node.category, node.importance, node.metadata, db)
                nodes.append(node)
            return nodes
        except Exception as exc:
            logger.warning("extract_facts failed: %s", exc)
            return []

    @staticmethod
    async def store_fact(
        user_id: str,
        fact: str,
        category: str,
        importance: float = 0.5,
        metadata: Dict = None,
        db: AsyncSession = None,
    ) -> MemoryFact:
        """Store a fact with its vector embedding. Skips duplicates."""
        if not fact.strip():
            return None

        # Skip exact duplicates
        if db:
            existing = await db.execute(
                select(MemoryFact).where(MemoryFact.user_id == user_id, MemoryFact.fact == fact)
            )
            if existing.scalar_one_or_none():
                return None

        embedding = await _embeddings.aembed_query(fact)

        memory_fact = MemoryFact(
            user_id=user_id,
            fact=fact,
            category=category,
            importance=importance,
            metadata_json=json.dumps(metadata or {}),
        )

        if db:
            db.add(memory_fact)
            await db.flush()

            memory_embedding = MemoryEmbedding(
                memory_fact_id=memory_fact.id,
                embedding=embedding,
            )
            db.add(memory_embedding)
            await db.commit()
            await db.refresh(memory_fact)

        return memory_fact

    @staticmethod
    async def search_semantic(user_id: str, query: str, db: AsyncSession, limit: int = 5) -> List[str]:
        """Semantic similarity search using pgvector L2 distance via ORM."""
        try:
            query_embedding = await _embeddings.aembed_query(query)
            stmt = (
                select(MemoryFact)
                .join(MemoryEmbedding, MemoryFact.id == MemoryEmbedding.memory_fact_id)
                .where(MemoryFact.user_id == user_id)
                .order_by(MemoryEmbedding.embedding.l2_distance(query_embedding))
                .limit(limit)
            )
            result = await db.execute(stmt)
            return [f.fact for f in result.scalars().all()]
        except Exception as exc:
            logger.warning("Semantic search failed: %s", exc)
            return []

    @staticmethod
    async def retrieve_relevant_facts(user_id: str, query: str, db: AsyncSession, limit: int = 10) -> List[str]:
        """Hybrid retrieval: semantic similarity + high-importance facts."""
        half = limit // 2
        semantic = await MemoryService.search_semantic(user_id, query, db, limit=half)

        stmt = (
            select(MemoryFact)
            .where(MemoryFact.user_id == user_id)
            .order_by(MemoryFact.importance.desc())
            .limit(half)
        )
        result = await db.execute(stmt)
        by_importance = [f.fact for f in result.scalars().all()]

        return list(dict.fromkeys(semantic + by_importance))  # deduplicate, preserve order

    @staticmethod
    async def get_memory_context(user_id: str, db: AsyncSession, min_importance: float = 0.4) -> str:
        """Return formatted memory context for the agent system prompt."""
        stmt = (
            select(MemoryFact)
            .where(MemoryFact.user_id == user_id, MemoryFact.importance >= min_importance)
            .order_by(MemoryFact.importance.desc())
            .limit(20)
        )
        result = await db.execute(stmt)
        facts = result.scalars().all()

        if not facts:
            return "No prior context available."

        by_category: Dict[str, List[str]] = {}
        for f in facts:
            by_category.setdefault(f.category, []).append(f.fact)

        lines = ["User Profile & Context:"]
        for cat, fact_list in by_category.items():
            lines.append(f"\n[{cat.upper()}]:")
            for fact in fact_list:
                lines.append(f"  • {fact}")
        return "\n".join(lines)

    @staticmethod
    async def get_constraint_context(user_id: str, db: AsyncSession) -> str:
        """Return only constraints and high-importance preferences for email/calendar drafting."""
        stmt = (
            select(MemoryFact)
            .where(
                MemoryFact.user_id == user_id,
                MemoryFact.category.in_(["preference", "constraint", "habit"]),
                MemoryFact.importance >= 0.7,
            )
            .order_by(MemoryFact.importance.desc())
        )
        result = await db.execute(stmt)
        facts = result.scalars().all()
        if not facts:
            return ""
        lines = ["User constraints and preferences:"]
        for f in facts:
            lines.append(f"  • {f.fact}")
        return "\n".join(lines)
