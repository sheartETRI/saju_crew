from __future__ import annotations

from typing import Any, Dict, Literal

from ..data_loader import load_yaml_resource

RESOURCE_PATH = "get_yinyang/yinyang_decision"


def get_yinyang(value: str) -> Dict[str, Literal["yin", "yang"]]:
    """Return yin/yang for a stem or branch."""
    data = load_yaml_resource(RESOURCE_PATH)
    if value in data.get("yin_values", []):
        return {"value": value, "yinyang": "yin"}
    if value in data.get("yang_values", []):
        return {"value": value, "yinyang": "yang"}
    return {"value": value, "error": "value must be a stem or branch"}


__all__ = ["get_yinyang"]
