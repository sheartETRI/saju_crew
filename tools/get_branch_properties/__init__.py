from __future__ import annotations

from typing import Any, Dict

from ..common import ensure_branch
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_branch_properties/branch_properties"


def get_branch_properties(branch: str) -> Dict[str, Any]:
    """Return basic properties for a branch."""
    branch = ensure_branch(branch)
    data = load_yaml_resource(RESOURCE_PATH)
    for item in data.get("branch_properties", []):
        if item.get("branch") == branch:
            return item
    return {"branch": branch, "error": "properties not found"}


__all__ = ["get_branch_properties"]
