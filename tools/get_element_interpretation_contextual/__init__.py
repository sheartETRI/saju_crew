from __future__ import annotations

from typing import Any, Dict

from ..common import ELEMENTS, STEM_TO_ELEMENT, ensure_element
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_element_interpretation_contextual/element_interpretation_contextual"


def get_element_interpretation_contextual(stem_or_element: str, context: str) -> Dict[str, Any]:
    """Return a short interpretation text for an element in a given context."""
    context = context.strip()
    data = load_yaml_resource(RESOURCE_PATH)
    element = stem_or_element
    if stem_or_element in STEM_TO_ELEMENT:
        element = STEM_TO_ELEMENT[stem_or_element]
    if element not in ELEMENTS:
        raise ValueError("stem_or_element must be a stem or five-element value")

    element_map: Dict[str, Dict[str, str]] = data.get("interpretations", {})
    element_contexts = element_map.get(element, {})
    text = element_contexts.get(context) or element_contexts.get("default")
    if not text:
        return {
            "element": element,
            "context": context,
            "error": "no interpretation for this context",
            "available_contexts": list(element_contexts.keys()),
        }
    return {
        "element": element,
        "context": context,
        "interpretation": text,
        "available_contexts": list(element_contexts.keys()),
    }


__all__ = ["get_element_interpretation_contextual"]
