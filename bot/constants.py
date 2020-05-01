from managedState.registrar import KeyQueryFactory

from .classes.timeoutDuration import TimeoutDuration

class Permissions:
    level_none = 0
    level_admin = 1

class KeyQueryFactories:
    dynamic_key = KeyQueryFactory(lambda sub_state, user_id: user_id)

class Defaults:
    state_filename = "data.json"

    timeout_duration = TimeoutDuration(1)

    permissions = {"level": Permissions.level_none, "tags": []}

class MessageFormats:
    welcome_header = "**Welcome back!**"
    cannot_find_user_identifier = "Unable to find a user based on the name: `{0}`"
    cannot_parse_timeout_string = "Unable to generate a timeout duration from the provided text: `{0}`"

class Methods:
    @staticmethod
    def clean(text):
        """Removes surrounding whitespace and any '\n's. Use to simplify dynamic inputs and outputs (e.g. usernames, command arguments)"""
        return text.strip().replace("\n", "")
