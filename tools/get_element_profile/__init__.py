from __future__ import annotations

from typing import Any, Dict

from ..common import ensure_element
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_element_profile/element_profile"


def get_element_profile(element: str) -> Dict[str, Any]:
    """Return profile information for an element."""
    element = ensure_element(element)
    data = load_yaml_resource(RESOURCE_PATH)
    for item in data.get("profiles", []):
        if item.get("element") == element:
            return item
    return {"element": element, "error": "profile not found"}


__all__ = ["get_element_profile"]
