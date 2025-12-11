"""Lookup helpers for ganji (천간/지지) trait data."""

from __future__ import annotations

import functools
from pathlib import Path
from typing import Dict, List, Literal, TypedDict

import yaml

# Trait data lives next to this module so it can be packaged together.
_TRAITS_PATH = Path(__file__).with_name("ganji_traits.yaml")


class TraitEntry(TypedDict, total=False):
    """Shape of the lookup result returned to agents/tools."""

    kind: Literal["stem", "branch"]
    code: str
    element: str | None
    yinyang: str | None
    traits: Dict[str, str]


@functools.lru_cache(maxsize=1)
def _load_traits(path: Path = _TRAITS_PATH) -> Dict:
    """Read and cache the trait YAML so repeated tool calls are fast."""
    if not path.exists():
        raise FileNotFoundError(f"Trait data not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Trait file is malformed: expected a mapping at the top level.")

    return data


def _find_match(items: List[Dict], code_field: str, code: str) -> Dict | None:
    """Locate the first entry whose code matches the requested character."""
    for item in items:
        if item.get(code_field) == code:
            return item
    return None


def get_ganji_traits(kind: str, code: str) -> TraitEntry:
    """Return element/yinyang/traits for a single stem or branch code."""
    normalized_kind = kind.strip().lower()
    if normalized_kind not in {"stem", "branch"}:
        raise ValueError("kind must be 'stem' or 'branch'")

    code = code.strip()
    data = _load_traits()

    list_key = "stems_traits" if normalized_kind == "stem" else "branch_traits"
    code_key = "stem" if normalized_kind == "stem" else "branch"
    available: List[Dict] = data.get(list_key, [])

    match = _find_match(available, code_key, code)
    if not match:
        return {
            "error": f"Unknown {normalized_kind} code: {code}",
            "available_codes": [item.get(code_key) for item in available],
        }

    return {
        "kind": normalized_kind,
        "code": code,
        "element": match.get("element"),
        "yinyang": match.get("yinyang"),
        "traits": match.get("traits", {}),
    }


__all__ = ["get_ganji_traits"]
