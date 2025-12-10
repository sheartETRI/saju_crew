"""
CrewAI-based agent that answers questions about 천간·지지 traits using the existing ganji lookup.

Prerequisites:
  pip install crewai crewai-tools openai pyyaml
Usage:
  python crew_agent_demo.py "卯는 어떤 성격인가요?"
  # or without an argument, it will run with a default sample question.
"""

import json
import signal
import sys
from pathlib import Path
from typing import Optional

# CrewAI accesses several POSIX-only signals; stub them on Windows.
if not hasattr(signal, "SIGHUP"):
    signal.SIGHUP = signal.SIGTERM  # type: ignore[attr-defined]
if not hasattr(signal, "SIGTSTP"):
    signal.SIGTSTP = signal.SIGTERM  # type: ignore[attr-defined]
if not hasattr(signal, "SIGCONT"):
    signal.SIGCONT = signal.SIGTERM  # type: ignore[attr-defined]

from pydantic import BaseModel, field_validator

from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool

from get_traits import get_ganji_traits


def load_tool_spec(path: str = "tools.json") -> dict:
    """Load the tool schema JSON (shared with agent_demo) to avoid drift."""
    return json.loads(Path(path).read_text(encoding="utf-8"))[0]["function"]


TOOL_SPEC = load_tool_spec()
TOOL_DESCRIPTION = TOOL_SPEC.get("description", "천간/지지 한 글자의 오행·음양·특성을 조회한다.")
CODE_ENUM = set(TOOL_SPEC.get("parameters", {}).get("properties", {}).get("code", {}).get("enum", []))
CODE_LIST_TEXT = ", ".join(sorted(CODE_ENUM))
TOOL_USAGE_GUIDE = (
    "도구 호출 전 정의를 확인하고 정확히 채워라: "
    f"{TOOL_SPEC.get('name', 'get_ganji_traits')}(kind: 'stem'|'branch', code: [{CODE_LIST_TEXT}])."
)


class GanjiArgs(BaseModel):
    kind: str
    code: str

    @field_validator("kind")
    @classmethod
    def validate_kind(cls, v: str) -> str:
        if v not in {"stem", "branch"}:
            raise ValueError("kind는 'stem' 또는 'branch'여야 합니다.")
        return v

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if CODE_ENUM and v not in CODE_ENUM:
            raise ValueError(f"code는 다음 중 하나여야 합니다: {sorted(CODE_ENUM)}")
        return v


class GanjiTool(BaseTool):
    name: str = "get_ganji_traits"
    description: str = TOOL_DESCRIPTION
    args_schema: type[BaseModel] = GanjiArgs

    def _run(self, kind: str, code: str) -> dict:
        return get_ganji_traits(kind, code)


def build_crew(model: str = "gpt-4o-mini") -> Crew:
    """Create the Crew with a single helper agent and one answering task."""
    ganji_tool = GanjiTool()

    helper = Agent(
        role="사주 도우미",
        goal="천간·지지의 오행·음양·특성을 알기 쉽게 안내한다.",
        backstory="사주를 처음 접하는 사람에게 기본 정보를 설명해주는 친절한 가이드.",
        tools=[ganji_tool],
        allow_delegation=False,
        verbose=False,
        model=model,
    )

    answer_task = Task(
        description=(
            "사용자 질문에 답변하라.\n"
            "질문: {question}\n"
            f"{TOOL_USAGE_GUIDE}\n"
            "kind/code 파라미터를 정확히 채운 뒤 도구를 호출하고, 결과를 한국어로 간결히 설명하라."
        ),
        expected_output="천간/지지의 오행·음양·특성을 한국어로 간결히 설명한다.",
        agent=helper,
    )

    return Crew(
        agents=[helper],
        tasks=[answer_task],
        process=Process.sequential,
        verbose=False,
    )


def run(question: str, model: str = "gpt-4o-mini") -> str:
    """Run the crew on a single question and return the answer text."""
    crew = build_crew(model=model)
    result = crew.kickoff(inputs={"question": question})
    return str(result)


if __name__ == "__main__":
    q: Optional[str] = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    question = q or "卯는 어떤 성격인가요?"
    print(run(question))