from __future__ import annotations

from typing import Any, Dict

from ..common import ensure_branch
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_hidden_stems/hidden_stems"


def get_hidden_stems(branch: str) -> Dict[str, Any]:
    """Return hidden stems for a branch."""
    branch = ensure_branch(branch)
    data = load_yaml_resource(RESOURCE_PATH)
    for item in data.get("hidden_stems", []):
        if item.get("branch") == branch:
            return item
    return {"branch": branch, "error": "hidden stems not found"}


__all__ = ["get_hidden_stems"]
