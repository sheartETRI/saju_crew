"""Shared constants and validation helpers for tool implementations."""

from __future__ import annotations

from typing import Dict, List

BRANCHES: List[str] = [
    "\u5b50",
    "\u4e11",
    "\u5bc5",
    "\u536f",
    "\u8fb0",
    "\u5df3",
    "\u5348",
    "\u672a",
    "\u7533",
    "\u9149",
    "\u620c",
    "\u4ea5",
]

ELEMENTS: List[str] = ["\u6728", "\u706b", "\u571f", "\u91d1", "\u6c34"]

STEMS: List[str] = [
    "\u7532",
    "\u4e59",
    "\u4e19",
    "\u4e01",
    "\u620a",
    "\u5df1",
    "\u5e9a",
    "\u8f9b",
    "\u58ec",
    "\u7678",
]

STEM_TO_ELEMENT: Dict[str, str] = {
    "\u7532": "\u6728",
    "\u4e59": "\u6728",
    "\u4e19": "\u706b",
    "\u4e01": "\u706b",
    "\u620a": "\u571f",
    "\u5df1": "\u571f",
    "\u5e9a": "\u91d1",
    "\u8f9b": "\u91d1",
    "\u58ec": "\u6c34",
    "\u7678": "\u6c34",
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
