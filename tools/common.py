"""Shared constants and validation helpers for tool implementations."""

from __future__ import annotations

from typing import Dict, List

BRANCHES: List[str] = [
    "子",
    "丑",
    "寅",
    "卯",
    "辰",
    "巳",
    "午",
    "未",
    "申",
    "酉",
    "戌",
    "亥",
]

ELEMENTS: List[str] = ["木", "火", "土", "金", "水"]

STEMS: List[str] = [
    "甲",
    "乙",
    "丙",
    "丁",
    "戊",
    "己",
    "庚",
    "辛",
    "壬",
    "癸",
]

STEM_TO_ELEMENT: Dict[str, str] = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水",
}


def ensure_branch(value: str) -> str:
    """Validate an earthly branch value."""
    if value not in BRANCHES:
        raise ValueError(f"branch must be one of {BRANCHES}")
    return value


def ensure_element(value: str) -> str:
    """Validate a five-element value."""
    if value not in ELEMENTS:
        raise ValueError(f"element must be one of {ELEMENTS}")
    return value


def ensure_stem(value: str) -> str:
    """Validate a heavenly stem value."""
    if value not in STEMS:
        raise ValueError(f"stem must be one of {STEMS}")
    return value


__all__ = [
    "BRANCHES",
    "ELEMENTS",
    "STEMS",
    "STEM_TO_ELEMENT",
    "ensure_branch",
    "ensure_element",
    "ensure_stem",
]
