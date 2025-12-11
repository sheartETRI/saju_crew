"""
CrewAI-based agent that answers questions about 천간·지지/오행 정보를 제공합니다.

Prerequisites:
  pip install crewai crewai-tools openai pyyaml
Usage:
  python crew_agent_demo.py "임수는 어떤 성격인가?"
  python crew_agent_demo.py --smoke        # 모든 툴 함수 스모크 테스트(직접 호출)
  python crew_agent_demo.py --test-all     # tools.json 순서대로 모든 툴을 연속 실행해 보기
"""

from __future__ import annotations

import signal
import sys
from typing import Any, Dict, List, Optional, Tuple

# CrewAI accesses several POSIX-only signals; stub them on Windows.
if not hasattr(signal, "SIGHUP"):
    signal.SIGHUP = signal.SIGTERM  # type: ignore[attr-defined]
if not hasattr(signal, "SIGTSTP"):
    signal.SIGTSTP = signal.SIGTERM  # type: ignore[attr-defined]
if not hasattr(signal, "SIGCONT"):
    signal.SIGCONT = signal.SIGTERM  # type: ignore[attr-defined]

from pydantic import BaseModel, create_model, field_validator

from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool

from tools import TOOL_REGISTRY, get_ganji_traits, load_tool_specs
from tools.common import BRANCHES, ELEMENTS, STEMS


# Load all specs once so we can derive names and a representative example.
ALL_TOOL_SPECS = load_tool_specs("tools.json")
TOOL_SPEC = ALL_TOOL_SPECS[0]["function"]
TOOL_NAMES = [spec["function"]["name"] for spec in ALL_TOOL_SPECS]
TOOL_DESCRIPTION = TOOL_SPEC.get("description", "천간/지지 코드의 특성을 조회합니다.")
CODE_ENUM = set(TOOL_SPEC.get("parameters", {}).get("properties", {}).get("code", {}).get("enum", []))
CODE_LIST_TEXT = ", ".join(sorted(CODE_ENUM))
TOOL_USAGE_GUIDE = (
    "사용 가능한 도구: "
    f"{', '.join(TOOL_NAMES)}. "
    "필요에 맞는 도구를 선택해 스펙에 정의된 파라미터로 호출하라 "
    f"(예시: {TOOL_SPEC.get('name', 'get_ganji_traits')}(kind: 'stem'|'branch', code: [{CODE_LIST_TEXT}]))."
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


def _pydantic_field(property_spec: Dict[str, Any], required: bool) -> Tuple[type, Any]:
    """Create a pydantic field tuple from an OpenAPI-style property spec."""
    t = str
    if property_spec.get("type") in {"integer", "number"}:
        t = int
    enum = property_spec.get("enum")
    if enum:
        try:
            from typing import Literal

            t = Literal[tuple(enum)]  # type: ignore[assignment]
        except Exception:
            t = str
    default = ... if required else None
    return t, default


def build_dynamic_tool(spec: Dict[str, Any]) -> BaseTool:
    """Build a CrewAI BaseTool from a tool spec and registry function."""
    tool_name = spec["name"]
    func = TOOL_REGISTRY[tool_name]
    params = spec.get("parameters", {}).get("properties", {})
    required_fields = set(spec.get("parameters", {}).get("required", []))

    model_fields = {
        field_name: _pydantic_field(prop_spec, field_name in required_fields)
        for field_name, prop_spec in params.items()
    }
    args_model = create_model(f"{tool_name}_Args", **model_fields)  # type: ignore[arg-type]

    def _run(self, **kwargs: Any) -> Any:  # type: ignore[override]
        return func(**kwargs)

    annotations = {
        "name": str,
        "description": str,
        "args_schema": type[BaseModel],
    }
    attrs = {
        "__annotations__": annotations,
        "__module__": __name__,
        "name": tool_name,
        "description": spec.get("description", ""),
        "args_schema": args_model,
        "_run": _run,
    }
    DynamicTool = type(f"{tool_name}_Tool", (BaseTool,), attrs)
    return DynamicTool()


def build_tools() -> List[BaseTool]:
    """Instantiate tools for all functions defined in tools.json."""
    specs = load_tool_specs("tools.json")
    tools: List[BaseTool] = []
    for spec_entry in specs:
        function_spec = spec_entry["function"]
        tools.append(build_dynamic_tool(function_spec))
    # Keep ganji tool (with stricter validation) first for backward compatibility
    tools.insert(0, GanjiTool())
    return tools


def build_crew(model: str = "gpt-4o-mini") -> Crew:
    """Create the Crew with a single helper agent and one answering task."""
    tools = build_tools()

    helper = Agent(
        role="사주 도우미",
        goal="천간·지지·오행 관련 질문을 정확히 답하고 필요한 계산을 수행한다.",
        backstory="사주를 처음 접하는 사람에게 기본 정보부터 간단한 해석까지 알려주는 도우미다.",
        tools=tools,
        allow_delegation=False,
        verbose=False,
        model=model,
    )

    answer_task = Task(
        description=(
            "사용자 질문에 답변하라.\n"
            "질문: {question}\n"
            f"{TOOL_USAGE_GUIDE}\n"
            "kind/code 파라미터 등을 확인하고, 결과를 한국어로 간결하게 설명하라."
        ),
        expected_output="천간/지지·오행 정보 또는 해석을 한국어로 간결히 답한다.",
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


def _sample_inputs() -> Dict[str, Dict[str, Any]]:
    """Provide sample inputs per tool for smoke testing."""
    return {
        "get_ganji_traits": {"kind": "stem", "code": STEMS[0]},
        "get_branch_element_strength": {"branch": BRANCHES[0], "element": ELEMENTS[0]},
        "get_branch_interaction": {"branch1": BRANCHES[0], "branch2": BRANCHES[1]},
        "get_month_branch": {"branch": BRANCHES[0]},
        "get_branch_properties": {"branch": BRANCHES[0]},
        "get_element_interpretation_contextual": {"stem_or_element": ELEMENTS[0], "context": "default"},
        "get_element_profile": {"element": ELEMENTS[0]},
        "get_five_element_relation": {"source": ELEMENTS[0], "target": ELEMENTS[1]},
        "get_hidden_stems": {"branch": BRANCHES[0]},
        "get_stem_purpose": {"stem": STEMS[0]},
    }


def smoke_test() -> None:
    """Call every tool once with representative inputs and print results."""
    samples = _sample_inputs()
    specs = {spec["function"]["name"]: spec["function"] for spec in load_tool_specs("tools.json")}
    for name, func in TOOL_REGISTRY.items():
        if name not in samples:
            continue
        args = samples[name]
        try:
            result = func(**args)
            print(f"[PASS] {name}({args}) -> {result}")
        except Exception as exc:  # pragma: no cover - dev-time smoke
            desc = specs.get(name, {}).get("description", "")
            print(f"[FAIL] {name}({args}) desc='{desc}': {exc}")


def test_all_tools_sequential() -> None:
    """Run all tools in tools.json order with sample inputs."""
    samples = _sample_inputs()
    specs = load_tool_specs("tools.json")
    for spec_entry in specs:
        func_spec = spec_entry["function"]
        name = func_spec["name"]
        func = TOOL_REGISTRY.get(name)
        if not func:
            print(f"[SKIP] {name}: not registered in TOOL_REGISTRY")
            continue
        args = samples.get(name)
        if not args:
            print(f"[SKIP] {name}: no sample input defined")
            continue
        try:
            result = func(**args)
            print(f"[PASS] {name}({args}) -> {result}")
        except Exception as exc:  # pragma: no cover - dev-time smoke
            print(f"[FAIL] {name}({args}) -> {exc}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--smoke":
        smoke_test()
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == "--test-all":
        test_all_tools_sequential()
        sys.exit(0)

    q: Optional[str] = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    question = q or "임수는 어떤 성격인가?"
    print(run(question))
