from __future__ import annotations

from typing import Any, Dict

from ..common import ensure_branch
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_branch_month/branch_month"


def get_branch_month(branch: str) -> Dict[str, Any]:
    """Return the month number associated with a branch."""
    branch = ensure_branch(branch)
    data = load_yaml_resource(RESOURCE_PATH)
    month = data.get("branch_to_month_map", {}).get(branch)
    if month is None:
        return {"branch": branch, "error": "month not defined"}
    return {"branch": branch, "month": month}


__all__ = ["get_branch_month"]
