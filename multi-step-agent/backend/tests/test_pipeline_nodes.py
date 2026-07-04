"""
Tests for multi-step-agent pipeline nodes.
LLM calls are mocked so tests run without network access or API keys.
"""
from __future__ import annotations

import asyncio
import json
from typing import List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agent.state import AgentState, StepLog


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_state(**overrides) -> AgentState:
    base: AgentState = {
        "goal": "research quantum computing advances in 2025",
        "search_queries": [],
        "search_results": [],
        "filtered_results": [],
        "summaries": [],
        "outline": "",
        "draft": "",
        "step_logs": [],
        "current_step": "planner",
        "status": "running",
        "error": None,
    }
    base.update(overrides)
    return base


def _llm_response(content: str) -> MagicMock:
    """Return a mock LLM response object whose .content is *content*."""
    mock = MagicMock()
    mock.content = content
    return mock


# ---------------------------------------------------------------------------
# AgentState schema
# ---------------------------------------------------------------------------

class TestAgentStateSchema:
    def test_required_fields_present(self):
        state = _make_state()
        required = {
            "goal", "search_queries", "search_results", "filtered_results",
            "summaries", "outline", "draft", "step_logs",
            "current_step", "status", "error",
        }
        assert required.issubset(state.keys())

    def test_step_log_schema(self):
        log: StepLog = {
            "step": "planner",
            "status": "complete",
            "output": "Generated 3 queries",
            "error": None,
        }
        assert log["step"] == "planner"
        assert log["error"] is None

    def test_error_field_is_optional_none(self):
        state = _make_state()
        assert state["error"] is None

    def test_state_passes_forward(self):
        """Simulate state accumulation across two nodes."""
        state = _make_state()

        # First node appends a log
        log1: StepLog = {"step": "planner", "status": "complete", "output": "ok", "error": None}
        updated = dict(state)
        updated["search_queries"] = ["query a", "query b"]
        updated["step_logs"] = state["step_logs"] + [log1]
        updated["current_step"] = "search"

        # Second node reads what first node wrote
        assert updated["search_queries"] == ["query a", "query b"]
        assert len(updated["step_logs"]) == 1
        assert updated["current_step"] == "search"


# ---------------------------------------------------------------------------
# planner_node
# ---------------------------------------------------------------------------

class TestPlannerNode:
    @pytest.fixture(autouse=True)
    def _patch_llm(self):
        """Patch _get_llm so planner_node never hits a real API."""
        queries = ["quantum computing 2025 breakthroughs", "quantum error correction progress", "IBM Google quantum milestone"]
        mock_llm = MagicMock()
        mock_llm.ainvoke = AsyncMock(return_value=_llm_response(json.dumps(queries)))
        with patch("app.agent.nodes._get_llm", return_value=mock_llm):
            yield mock_llm

    def test_planner_returns_nonempty_queries(self):
        from app.agent.nodes import planner_node

        state = _make_state()
        result = asyncio.get_event_loop().run_until_complete(planner_node(state))

        assert "search_queries" in result
        queries: List[str] = result["search_queries"]
        assert len(queries) > 0, "planner must produce at least one search query"

    def test_planner_queries_are_strings(self):
        from app.agent.nodes import planner_node

        state = _make_state()
        result = asyncio.get_event_loop().run_until_complete(planner_node(state))

        for q in result["search_queries"]:
            assert isinstance(q, str)

    def test_planner_appends_step_log(self):
        from app.agent.nodes import planner_node

        state = _make_state()
        result = asyncio.get_event_loop().run_until_complete(planner_node(state))

        logs = result["step_logs"]
        assert len(logs) == 1
        assert logs[0]["step"] == "planner"
        assert logs[0]["status"] == "complete"

    def test_planner_sets_next_step(self):
        from app.agent.nodes import planner_node

        state = _make_state()
        result = asyncio.get_event_loop().run_until_complete(planner_node(state))

        assert result["current_step"] == "search"


# ---------------------------------------------------------------------------
# filter_node — removes off-topic results
# ---------------------------------------------------------------------------

class TestFilterNode:
    def _make_results(self) -> list[dict]:
        return [
            {"url": "https://a.com", "title": "Quantum error correction breakthrough", "snippet": "Researchers achieve fault-tolerant qubit arrays."},
            {"url": "https://b.com", "title": "Best pasta recipes 2025", "snippet": "Spaghetti carbonara tips."},
            {"url": "https://c.com", "title": "IBM unveils 1000-qubit processor", "snippet": "New quantum chip sets speed record."},
            {"url": "https://d.com", "title": "Celebrity gossip weekly", "snippet": "Tabloid news unrelated to science."},
            {"url": "https://e.com", "title": "Google quantum supremacy revisited", "snippet": "Analysis of Google's latest quantum experiments."},
        ]

    @pytest.fixture(autouse=True)
    def _patch_llm(self):
        # Simulate LLM returning indices 0, 2, 4 (the on-topic results)
        mock_llm = MagicMock()
        mock_llm.ainvoke = AsyncMock(return_value=_llm_response(json.dumps([0, 2, 4])))
        with patch("app.agent.nodes._get_llm", return_value=mock_llm):
            yield mock_llm

    def test_filter_removes_irrelevant_results(self):
        from app.agent.nodes import filter_node

        results = self._make_results()
        state = _make_state(search_results=results)
        result = asyncio.get_event_loop().run_until_complete(filter_node(state))

        filtered = result["filtered_results"]
        titles = [r["title"] for r in filtered]
        assert "Best pasta recipes 2025" not in titles
        assert "Celebrity gossip weekly" not in titles

    def test_filter_keeps_relevant_results(self):
        from app.agent.nodes import filter_node

        results = self._make_results()
        state = _make_state(search_results=results)
        result = asyncio.get_event_loop().run_until_complete(filter_node(state))

        filtered = result["filtered_results"]
        titles = [r["title"] for r in filtered]
        assert "Quantum error correction breakthrough" in titles
        assert "IBM unveils 1000-qubit processor" in titles

    def test_filter_result_count_bounded(self):
        from app.agent.nodes import filter_node

        results = self._make_results()
        state = _make_state(search_results=results)
        result = asyncio.get_event_loop().run_until_complete(filter_node(state))

        assert len(result["filtered_results"]) <= 5

    def test_filter_appends_step_log(self):
        from app.agent.nodes import filter_node

        state = _make_state(search_results=self._make_results())
        result = asyncio.get_event_loop().run_until_complete(filter_node(state))

        logs = result["step_logs"]
        assert any(l["step"] == "filter" for l in logs)


# ---------------------------------------------------------------------------
# draft_node — returns a non-empty string
# ---------------------------------------------------------------------------

class TestDraftNode:
    SAMPLE_OUTLINE = """## Introduction
- Background on quantum computing
## Key Advances in 2025
- Error correction milestones
- Qubit count records
## Conclusion
- Industry impact
"""

    @pytest.fixture(autouse=True)
    def _patch_llm(self):
        draft_text = (
            "Quantum computing saw remarkable progress in 2025. "
            "Researchers at IBM and Google demonstrated fault-tolerant qubits "
            "and broke the 1000-qubit barrier, marking a turning point for the field."
        )
        mock_llm = MagicMock()
        mock_llm.ainvoke = AsyncMock(return_value=_llm_response(draft_text))
        with patch("app.agent.nodes._get_llm", return_value=mock_llm):
            yield mock_llm

    def test_draft_returns_nonempty_string(self):
        from app.agent.nodes import draft_node

        state = _make_state(outline=self.SAMPLE_OUTLINE)
        result = asyncio.get_event_loop().run_until_complete(draft_node(state))

        assert "draft" in result
        assert isinstance(result["draft"], str)
        assert len(result["draft"].strip()) > 0

    def test_draft_status_set_complete(self):
        from app.agent.nodes import draft_node

        state = _make_state(outline=self.SAMPLE_OUTLINE)
        result = asyncio.get_event_loop().run_until_complete(draft_node(state))

        assert result["status"] == "complete"
        assert result["current_step"] == "done"

    def test_draft_appends_step_log(self):
        from app.agent.nodes import draft_node

        state = _make_state(outline=self.SAMPLE_OUTLINE)
        result = asyncio.get_event_loop().run_until_complete(draft_node(state))

        logs = result["step_logs"]
        assert any(l["step"] == "draft" for l in logs)


# ---------------------------------------------------------------------------
# _parse_json_response — pure function, no mock needed
# ---------------------------------------------------------------------------

class TestParseJsonResponse:
    def test_plain_json_array(self):
        from app.agent.nodes import _parse_json_response

        result = _parse_json_response('["query one", "query two", "query three"]')
        assert result == ["query one", "query two", "query three"]

    def test_json_wrapped_in_code_fence(self):
        from app.agent.nodes import _parse_json_response

        text = "```json\n[1, 2, 3]\n```"
        result = _parse_json_response(text)
        assert result == [1, 2, 3]

    def test_plain_code_fence(self):
        from app.agent.nodes import _parse_json_response

        text = "```\n[\"a\", \"b\"]\n```"
        result = _parse_json_response(text)
        assert result == ["a", "b"]

    def test_whitespace_stripped(self):
        from app.agent.nodes import _parse_json_response

        result = _parse_json_response('  [0, 2, 4]  ')
        assert result == [0, 2, 4]

    def test_invalid_json_raises(self):
        from app.agent.nodes import _parse_json_response

        with pytest.raises(Exception):
            _parse_json_response("not valid json")
