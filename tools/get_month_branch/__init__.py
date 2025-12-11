from __future__ import annotations

from typing import Any, Dict

from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_month_branch/month_branch"


def get_month_branch(month: int) -> Dict[str, Any]:
    """Return the branch associated with a month number (1-12)."""
    month_number = int(month)
    if not 1 <= month_number <= 12:
        raise ValueError("month must be between 1 and 12")
    data = load_yaml_resource(RESOURCE_PATH)
    branch = data.get("month_to_branch_map", {}).get(month_number)
    if not branch:
        return {"month": month_number, "error": "branch not defined"}
    return {"month": month_number, "branch": branch}


__all__ = ["get_month_branch"]
