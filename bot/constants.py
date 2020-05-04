from managedState.registrar import KeyQueryFactory

from .classes.timeoutDuration import TimeoutDuration
from .classes.permissions import Permissions

class KeyQueryFactories:
    dynamic_key = KeyQueryFactory(lambda sub_state, user_id: user_id)

class Defaults:
    state_filename = "data.json"

    timeout_duration = TimeoutDuration(1)

    permissions = Permissions(Permissions.level_none, [])

class Methods:
    @staticmethod
    def clean(text):
        """Removes surrounding whitespace and any '\n's. Use to simplify dynamic inputs and outputs (e.g. usernames, command arguments)"""
        return text.strip().replace("\n", "")

class MessageFormats:
    format__list_item = "'**{0}**'"
    format__user_input = "`{0}`"