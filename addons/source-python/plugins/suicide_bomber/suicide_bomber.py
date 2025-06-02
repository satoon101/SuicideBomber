# ../suicide_bomber/suicide_bomber.py

"""Plugin that allows the bomb carrier to detonate at any time."""
# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from commands import CommandReturn
from commands.client import ClientCommand
from cvars import ConVar
from engines.sound import Sound
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.helpers import index_from_pointer
from entities.hooks import EntityCondition, EntityPreHook
from events import Event
from listeners import OnButtonStateChanged
from listeners.tick import Delay
from memory import make_object
from players.constants import PlayerButtons
from players.entity import Player
from players.helpers import index_from_userid

# Plugin
from .config import magnitude, radius, sound_file, sprite_scale


sound = Sound(str(sound_file), download=True)
mp_friendlyfire = ConVar("mp_friendlyfire")


class SuicideBomber:
    """Class used to handle suicide bomber functionality."""

    delays = {}
    attacker_index = None
    sequence_enabled = False

    def check_start_sequence(self, player):
        """Start the bombing sequence, if necessary."""
        if player.in_bomb_zone:
            return

        if player.active_weapon is None:
            return

        if player.active_weapon.classname != "weapon_c4":
            return

        sound.channel = player.index
        sound.index = player.index
        sound.play()
        self.delays[player.index] = Delay(
            delay=sound.duration,
            callback=self.explode_bomb,
            args=(player.index,),
        )

    def check_drop(self, index):
        """Disallow dropping the bomb."""
        if index not in self.delays:
            return CommandReturn.CONTINUE

        player = Player(index)
        if player.active_weapon is None:
            return CommandReturn.CONTINUE

        if player.active_weapon.classname != "weapon_c4":
            return CommandReturn.CONTINUE

        return CommandReturn.BLOCK

    def check_switch_weapons(self, index):
        """Disallow switching weapons for the bomber."""
        if index not in self.delays:
            return None

        return False

    def explode_bomb(self, index):
        """Create the explosion."""
        self.delays.pop(index, None)
        player = Player(index)
        player.active_weapon.remove()
        pointer = player.give_named_item("env_explosion")
        entity = make_object(Entity, pointer)
        entity.magnitude = int(magnitude)
        entity.radius_override = int(radius)
        entity.sprite_scale = int(sprite_scale)
        entity.spawn()
        entity.teleport(origin=player.origin)
        self.attacker_index = index
        entity.explode()
        self.attacker_index = None

    def check_damage(self, stack_data):
        """Update the inflictor/attacker if necessary."""
        if self.attacker_index is None:
            return

        victim = make_object(Entity, stack_data[0])
        if victim.classname != "player":
            return

        victim = Player(victim.index)
        attacker = Player(self.attacker_index)
        if (
            victim.team_index != attacker.team_index
            or int(mp_friendlyfire)
        ):
            take_damage_info = make_object(TakeDamageInfo, stack_data[1])
            take_damage_info.inflictor = self.attacker_index
            take_damage_info.attacker = self.attacker_index

    def cancel_bombing(self, index):
        """Cancel the delay and stop the sound."""
        sound.stop(index=index, channel=index)
        delay = self.delays.pop(index, None)
        if delay is not None:
            delay.cancel()


suicide_bomber = SuicideBomber()


@Event("player_death")
def stop_sound(game_event):
    """Cancel the delay."""
    suicide_bomber.cancel_bombing(
        index=index_from_userid(game_event["userid"]),
    )


@Event("round_start")
def disable_sequence(game_event):
    """Disable bombing during round freeze."""
    suicide_bomber.sequence_enabled = False


@Event("round_freeze_end")
def enable_sequence(game_event):
    """Re-enable bombing now that round freeze is over."""
    suicide_bomber.sequence_enabled = True


@OnButtonStateChanged
def on_button_state_changed(player, old_buttons, new_buttons):
    """Use button changes to start/stop the bombing sequence."""
    if not suicide_bomber.sequence_enabled:
        return
    if (
        not old_buttons & PlayerButtons.ATTACK
        and new_buttons & PlayerButtons.ATTACK
    ):
        suicide_bomber.check_start_sequence(player=player)

    elif (
        old_buttons & PlayerButtons.ATTACK and
        not new_buttons & PlayerButtons.ATTACK
    ):
        suicide_bomber.cancel_bombing(index=player.index)


@ClientCommand("drop")
def disable_drop(command, index):
    """Disallow dropping the bomb while in sequence."""
    return suicide_bomber.check_drop(index=index)


@EntityPreHook(EntityCondition.is_human_player, "weapon_switch")
def _pre_weapon_switch(stack_data):
    """Disallow switching weapons while in sequence."""
    return suicide_bomber.check_switch_weapons(
        index=index_from_pointer(stack_data[0]),
    )


@EntityPreHook(EntityCondition.is_bot_player, "on_take_damage")
@EntityPreHook(EntityCondition.is_human_player, "on_take_damage")
def _pre_take_damage(stack_data):
    """Update the inflictor/attacker if it is the bomb detonating."""
    suicide_bomber.check_damage(stack_data)
