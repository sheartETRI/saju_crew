from __future__ import annotations

from typing import Any, Dict

from ..common import ensure_branch, ensure_element
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_branch_element_strength/branch_element_strength"


def get_branch_element_strength(branch: str, element: str) -> Dict[str, Any]:
    """Return the qualitative strength of an element within a branch."""
    branch = ensure_branch(branch)
    element = ensure_element(element)
    data = load_yaml_resource(RESOURCE_PATH)
    strength = data.get("strength_map", {}).get(branch, {}).get(element)
    if not strength:
        return {
            "branch": branch,
            "element": element,
            "error": "strength not defined for this combination",
        }
    return {"branch": branch, "element": element, "strength": strength}


__all__ = ["get_branch_element_strength"]
