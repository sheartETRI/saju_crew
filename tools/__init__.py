"""Tool package for ganji-related utilities and future extensions."""

from .get_branch_element_strength import get_branch_element_strength
from .get_branch_interaction import get_branch_interaction
from .get_branch_properties import get_branch_properties
from .get_element_interpretation_contextual import get_element_interpretation_contextual
from .get_element_profile import get_element_profile
from .get_five_element_relation import get_five_element_relation
from .get_ganji_traits import get_ganji_traits
from .get_hidden_stems import get_hidden_stems
from .get_month_branch import get_month_branch
from .get_stem_purpose import get_stem_purpose
from .spec_loader import load_tool_specs

TOOL_REGISTRY = {
    "get_ganji_traits": get_ganji_traits,
    "get_branch_element_strength": get_branch_element_strength,
    "get_branch_interaction": get_branch_interaction,
    "get_month_branch": get_month_branch,
    "get_branch_properties": get_branch_properties,
    "get_element_interpretation_contextual": get_element_interpretation_contextual,
    "get_element_profile": get_element_profile,
    "get_five_element_relation": get_five_element_relation,
    "get_hidden_stems": get_hidden_stems,
    "get_stem_purpose": get_stem_purpose,
}

__all__ = [
    "get_ganji_traits",
    "get_branch_element_strength",
    "get_branch_interaction",
    "get_month_branch",
    "get_branch_properties",
    "get_element_interpretation_contextual",
    "get_element_profile",
    "get_five_element_relation",
    "get_hidden_stems",
    "get_stem_purpose",
    "load_tool_specs",
    "TOOL_REGISTRY",
]
