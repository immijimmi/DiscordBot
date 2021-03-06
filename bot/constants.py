from managedState.registrar import KeyQueryFactory

class KeyQueryFactories:
    dynamic_key = KeyQueryFactory(lambda sub_state, user_id: user_id)

class Methods:
    @staticmethod
    def clean(text):
        """Removes surrounding whitespace and any '\n's. Use to simplify dynamic inputs and outputs (e.g. usernames, command arguments)"""
        return text.strip().replace("\n", "")

class MessageFormats:
    format__list_item = "'**{0}**'"
    format__user_input = "`{0}`"
    format__note = "*{0}*"

    note__help = format__note.format("Type `!help` to see a list of commands.")

    unrecognised_command__user_input = "Unrecognised command: " + format__user_input + "\n" + note__help