from __future__ import annotations

from typing import Any, Dict, List

from ..common import ensure_branch
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_branch_interaction/branch_interaction"
RELATION_PRIORITY: List[str] = ["합", "충", "형", "파", "해"]


def get_branch_interaction(branch1: str, branch2: str) -> Dict[str, Any]:
    """Return the primary relation between two branches."""
    branch1 = ensure_branch(branch1)
    branch2 = ensure_branch(branch2)
    if branch1 == branch2:
        return {"relation": "same", "pair": [branch1, branch2]}

    data = load_yaml_resource(RESOURCE_PATH)
    relations: Dict[str, List[List[str]]] = data.get("relations", {})

    def _matches(pair: List[str]) -> bool:
        return set(pair) == {branch1, branch2}

    for relation_name in RELATION_PRIORITY:
        for pair in relations.get(relation_name, []):
            if _matches(pair):
                return {"relation": relation_name, "pair": [branch1, branch2]}

    return {"relation": "none", "pair": [branch1, branch2]}


__all__ = ["get_branch_interaction"]
