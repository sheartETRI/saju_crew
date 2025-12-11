from __future__ import annotations

from typing import Any, Dict, Mapping

from ..common import ensure_branch
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_month_branch/month_branch"


def _normalize_month_map(raw: Mapping[Any, Any]) -> Dict[int, str]:
    """Ensure month keys are ints even if the YAML loader returned strings."""
    return {int(key): str(value) for key, value in raw.items()}


def get_month_branch(month: int | None = None, branch: str | None = None) -> Dict[str, Any]:
    """Return the branch for a month number (1-12) or the month number for a branch."""
    if (month is None and branch is None) or (month is not None and branch is not None):
        raise ValueError("provide exactly one of month or branch")

    data = load_yaml_resource(RESOURCE_PATH)
    month_map = _normalize_month_map(data.get("month_to_branch_map", {}))
    branch_map = data.get("branch_to_month_map") or {v: k for k, v in month_map.items()}

    if month is not None:
        month_number = int(month)
        if not 1 <= month_number <= 12:
            raise ValueError("month must be between 1 and 12")
        branch_value = month_map.get(month_number)
        if not branch_value:
            return {"month": month_number, "error": "branch not defined"}
        return {"month": month_number, "branch": branch_value}

    branch_value = ensure_branch(str(branch))
    month_number = branch_map.get(branch_value)
    if month_number is None:
        return {"branch": branch_value, "error": "month not defined"}
    return {"branch": branch_value, "month": int(month_number)}


__all__ = ["get_month_branch"]
