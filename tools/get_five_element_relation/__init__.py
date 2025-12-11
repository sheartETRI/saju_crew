from __future__ import annotations

from typing import Any, Dict

from ..common import ensure_element
from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_five_element_relation/five_element_relation"


def get_five_element_relation(source: str, target: str) -> Dict[str, Any]:
    """두 오행의 관계가 생/극/같음인지 반환합니다."""
    source = ensure_element(source)
    target = ensure_element(target)
    if source == target:
        return {"source": source, "target": target, "relation": "same"}

    data = load_yaml_resource(RESOURCE_PATH)
    relation_map = data.get("relations", {})
    if relation_map.get("생", {}).get(source) == target:
        return {"source": source, "target": target, "relation": "생"}
    if relation_map.get("극", {}).get(source) == target:
        return {"source": source, "target": target, "relation": "극"}

    return {"source": source, "target": target, "relation": "none"}


__all__ = ["get_five_element_relation"]
