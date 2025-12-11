"""
Simple function-calling agent that answers questions about 천간·지지 traits.

Usage:
  1) Set OPENAI_API_KEY in your environment.
  2) Run: `python agent_demo.py`
"""

import json
from typing import Callable, Dict, List

from openai import OpenAI

from tools import TOOL_REGISTRY, load_tool_specs

client = OpenAI()


def load_tools(tools_path: str = "tools.json") -> List[Dict]:
    """Load the tool schema (supports $include for per-tool spec files)."""
    return load_tool_specs(tools_path)


TOOLS: List[Dict] = load_tools()


def handle_tool_call(tool_name: str, raw_arguments: str) -> Dict:
    """Dispatch the tool call to the local lookup functions."""
    args = json.loads(raw_arguments)
    fn: Callable | None = TOOL_REGISTRY.get(tool_name)
    if not fn:
        return {"error": f"Unknown tool: {tool_name}"}
    return fn(**args)


def run_agent(question: str, model: str = "gpt-4o-mini") -> str:
    """One-turn agent run: ask, let the model call tools, and return the final answer text."""
    messages = [
        {
            "role": "system",
            "content": "너는 사주 초보자를 돕는 도우미다. 필요하면 제공된 함수로 천간/지지 정보를 조회해라.",
        },
        {"role": "user", "content": question},
    ]

    first = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    message = first.choices[0].message
    print("=== First response ===")
    print(message)
    messages.append(message)

    if not message.tool_calls:
        return message.content or ""

    # Execute each tool call and append results so the model can cite them.
    for tool_call in message.tool_calls:
        tool_result = handle_tool_call(tool_call.function.name, tool_call.function.arguments)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": json.dumps(tool_result, ensure_ascii=False, indent=2),
            }
        )

    second = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return second.choices[0].message.content or ""


if __name__ == "__main__":
    question = "卯는 어떤 성격인가요?"
    answer = run_agent(question)
    print(answer)
