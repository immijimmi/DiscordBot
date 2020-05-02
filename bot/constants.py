from managedState.registrar import KeyQueryFactory

from .classes.timeoutDuration import TimeoutDuration
from .classes.permissions import Permissions

class KeyQueryFactories:
    dynamic_key = KeyQueryFactory(lambda sub_state, user_id: user_id)

class Defaults:
    state_filename = "data.json"

    timeout_duration = TimeoutDuration(1)

    permissions = Permissions(Permissions.level_none, [])

class MessageFormats:
    welcome_header = "**Welcome back!**"
    cannot_find_user_identifier = "Unable to find a user based on the name: `{0}`"
    cannot_parse_timeout_string = "Unable to get a timeout duration from the provided value: `{0}`\nTimeout duration must be a number of seconds between 1 and " + str(TimeoutDuration.max_seconds) + "."

    toggle_change_strings = ["toggle"]
    toggle_on_strings = ["on", "enable", "enabled"]
    toggle_off_strings = ["off", "disable", "disabled"]

class Methods:
    @staticmethod
    def clean(text):
        """Removes surrounding whitespace and any '\n's. Use to simplify dynamic inputs and outputs (e.g. usernames, command arguments)"""
        return text.strip().replace("\n", "")
