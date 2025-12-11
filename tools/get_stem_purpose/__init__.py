from __future__ import annotations

from typing import Any, Dict

from ..common import ensure_stem
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_stem_purpose/stem_purpose"


def get_stem_purpose(stem: str) -> Dict[str, Any]:
    """Return recommended usage and balancing elements for a stem."""
    stem = ensure_stem(stem)
    data = load_yaml_resource(RESOURCE_PATH)
    for item in data.get("stem_purpose", []):
        if item.get("stem") == stem:
            return item
    return {"stem": stem, "error": "purpose not found"}


__all__ = ["get_stem_purpose"]
