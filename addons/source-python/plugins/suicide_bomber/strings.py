# ../death_beam/strings.py

"""Contains all translation variables for the plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from translations.strings import LangStrings

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "CONFIG_STRINGS",
    "TRANSLATION_STRINGS",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
CONFIG_STRINGS = LangStrings(f"{info.name}/config_strings")
TRANSLATION_STRINGS = LangStrings(f"{info.name}/strings")
