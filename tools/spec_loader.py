"""Helpers for loading tool specs (with $include support)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _expand_includes(obj: Any, base_dir: Path) -> List[Any]:
    """Expand $include entries recursively, returning a flat list."""
    if isinstance(obj, list):
        expanded: List[Any] = []
        for item in obj:
            expanded.extend(_expand_includes(item, base_dir))
        return expanded

    if isinstance(obj, dict) and "$include" in obj:
        include_path = (base_dir / obj["$include"]).resolve()
        included = _load_json(include_path)
        return _expand_includes(included, include_path.parent)

    # Non-list, non-include items are returned as singletons.
    return [obj]


def load_tool_specs(tools_path: str | Path = "tools.json") -> List[Any]:
    """Load tool specs, allowing $include to pull in files from the tools dir."""
    path = Path(tools_path)
    parsed = _load_json(path)
    return _expand_includes(parsed, path.parent)


__all__ = ["load_tool_specs"]
