# ../suicide_bomber/config.py

"""Creates server configuration and user settings."""

# ==============================================================================
# >> IMPORTS
# ==============================================================================
# Source.Python
from config.manager import ConfigManager

# Plugin
from .info import info
from .strings import CONFIG_STRINGS

# ==============================================================================
# >> ALL DECLARATION
# ==============================================================================
__all__ = (
    "magnitude",
    "radius",
    "sound_file",
    "sprite_scale",
)


# ==============================================================================
# >> CONFIGURATION
# ==============================================================================
# Create the suicide_bomber.cfg file and execute it upon __exit__
with ConfigManager(info.name, "sb_") as _config:
    magnitude = _config.cvar(
        name="magnitude",
        default=1000,
        description=CONFIG_STRINGS["magnitude"],
    )
    radius = _config.cvar(
        name="radius",
        default=1000,
        description=CONFIG_STRINGS["radius"],
    )
    sprite_scale = _config.cvar(
        name="sprite_scale",
        default=100,
        description=CONFIG_STRINGS["sprite_scale"],
    )
    sound_file = _config.cvar(
        name="sound_file",
        default="source-python/suicide_bomber/suicide_bomber.mp3",
        description=CONFIG_STRINGS["sound_file"],
    )
