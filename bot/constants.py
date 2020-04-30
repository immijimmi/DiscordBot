from managedState.registrar import KeyQueryFactory

class Permissions:
    level_none = 0
    level_admin = 1

class KeyQueryFactories:
    dynamic_key = KeyQueryFactory(lambda sub_state, user_id: user_id)

class Defaults:
    state_filename = "data.json"

    timeout_duration = 1

    permissions = {"level": Permissions.level_none, "tags": []}

class MessageFormats:
    welcome_header = "**Welcome back!**"
    cannot_find_user_identifier = "Unable to find a user based on the name: `{0}`"

class Methods:
    @staticmethod
    def clean(text):
        """Removes surrounding whitespace and any '\n's. Use to simplify dynamic inputs and outputs (e.g. usernames, command arguments)"""
        return text.strip().replace("\n", "")

    @staticmethod
    def timeout_duration_string(seconds):
        if not seconds:
            return "{0} seconds".format(seconds)

        minutes = int(seconds/60)
        seconds -= minutes*60

        hours = int(minutes/60)
        minutes -= hours*60

        days = int(hours/24)
        hours -= days*24

        segment_lookup = {"days": days, "hours": hours, "minutes": minutes, "seconds": seconds}
        segments = [
            "{0} {1}".format(segment_lookup[segment_key], segment_key)
            for segment_key in ("days", "hours", "minutes", "seconds")
            if segment_lookup[segment_key] > 0
            ]

        return ", ".join(segments)