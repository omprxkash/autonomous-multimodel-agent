from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.models.memory import MemoryFact, MemoryEmbedding
from app.services.embeddings import embed_text, embed_query
import uuid

SIMILARITY_THRESHOLD = 0.85
TOP_K = 5


async def retrieve_relevant_memories(user_id: str, query: str, db: AsyncSession) -> str:
    try:
        query_vec = await embed_query(query)
        vec_str = f"[{','.join(str(v) for v in query_vec)}]"

        rows = await db.execute(
            text(
                """
                SELECT mf.content, mf.category, mf.importance,
                       1 - (me.vector <-> :vec::vector) AS similarity
                FROM memory_facts mf
                JOIN memory_embeddings me ON me.fact_id = mf.id
                WHERE mf.user_id = :uid
                ORDER BY me.vector <-> :vec::vector
                LIMIT :k
                """
            ),
            {"vec": vec_str, "uid": user_id, "k": TOP_K},
        )
        facts = rows.fetchall()
        if not facts:
            return ""
        return "\n".join(f"[{f.category}] {f.content}" for f in facts)
    except Exception:
        return ""


async def save_memory_fact(
    user_id: str,
    content: str,
    category: str,
    importance: float,
    db: AsyncSession,
) -> None:
    existing = await db.execute(
        select(MemoryFact).where(
            MemoryFact.user_id == user_id,
            MemoryFact.content == content,
        )
    )
    if existing.scalar_one_or_none():
        return

    fact = MemoryFact(
        id=str(uuid.uuid4()),
        user_id=user_id,
        category=category,
        content=content,
        importance=importance,
    )
    db.add(fact)
    await db.flush()

    vector = await embed_text(content)
    vec_str = f"[{','.join(str(v) for v in vector)}]"

    emb = MemoryEmbedding(id=str(uuid.uuid4()), fact_id=fact.id)
    db.add(emb)
    await db.flush()

    await db.execute(
        text("UPDATE memory_embeddings SET vector = :vec::vector WHERE id = :id"),
        {"vec": vec_str, "id": emb.id},
    )
    await db.commit()
