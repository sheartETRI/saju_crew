"""Shared helpers for loading YAML resources in the tools package."""

from __future__ import annotations

from __future__ import annotations

import functools
from pathlib import Path
from typing import Any, Dict

import yaml

TOOLS_DIR = Path(__file__).parent


@functools.lru_cache(maxsize=None)
def load_yaml_resource(relative_path: str) -> Dict[str, Any]:
    """Load and cache a YAML file stored under the tools directory."""
    path = TOOLS_DIR / relative_path
    if path.suffix == "":
        path = path.with_suffix(".yaml")
    if not path.exists():
        raise FileNotFoundError(f"YAML resource not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML resource '{relative_path}' must have a top-level mapping.")
    return data


__all__ = ["load_yaml_resource", "TOOLS_DIR"]
