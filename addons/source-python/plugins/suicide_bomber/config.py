# ../suicide_bomber/config.py

"""Creates server configuration and user settings."""

# ==============================================================================
# >> IMPORTS
# ==============================================================================
# Source.Python
from config.manager import ConfigManager

# Plugin
from .info import info

# ==============================================================================
# >> ALL DECLARATION
# ==============================================================================
__all__ = (
    "magnitude",
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
    )
    sprite_scale = _config.cvar(
        name="sprite_scale",
        default=100,
    )
    sound_file = _config.cvar(
        name="sound_file",
        default="source-python/suicide_bomber/suicide_bomber.mp3",
    )
