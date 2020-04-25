from managedState.registrar import KeyQueryFactory

class KeyQueryFactories:
    dynamic_key = KeyQueryFactory(lambda sub_state, user_id: user_id)

class Defaults:
    state_filename = "data.json"

    timeout_duration = 1

class MessageFormats:
    welcome_header = "**Welcome back!**"
    cannot_find_user_identifier = "Unable to find a user based on the name: `{0}`"

class Methods:
    @staticmethod
    def sanitise_message(message):
        return message.strip().replace("\n", "")
