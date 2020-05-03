from ..classes.timeoutDuration import TimeoutDuration
from ..constants import Methods
from .constants import MessageFormats, Arguments
from .handlerPlugin import HandlerPlugin

class Essentials(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self._event_methods["process_private_message"] += [
            self._private_message_welcome, self._private_message_welcome_toggle, self._private_message_welcome_timeout_change,
            self._private_message_nicknames_add
            ]

    def _private_message_welcome(self, message, handler_response=None):
        command = "!welcome"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                settings_string = "**Welcome Message Settings:**" + "\n"

                welcome_status = "enabled" if self.handler.state.registered_get("user_welcome_enabled", [str(message.author.id)]) else "disabled"
                settings_string += "status: " + "`" + welcome_status + "`" + "\n"

                timeout_duration = TimeoutDuration(self.handler.state.registered_get("user_welcome_timeout_seconds", [str(message.author.id)]))
                settings_string += "timeout duration: " + "`" + timeout_duration.to_user_string() + "`"

                handler_response.add(settings_string)

    def _private_message_welcome_toggle(self, message, handler_response=None):
        command = "!welcome "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                toggle_string = Methods.clean(message.content[len(command):])

                if toggle_string.lower() in MessageFormats.toggle_on_strings:
                    setting_enabled = True
                elif toggle_string.lower() in MessageFormats.toggle_off_strings:
                    setting_enabled = False
                elif toggle_string.lower() in MessageFormats.toggle_change_strings:
                    setting_enabled = not self.handler.state.registered_get("user_welcome_enabled", [str(message.author.id)])
                else:
                    return

                self.handler.state.registered_set(setting_enabled, "user_welcome_enabled", [str(message.author.id)])
                handler_response.add("Welcome messages {0}.".format("enabled" if setting_enabled else "disabled"))

    def _private_message_welcome_timeout_change(self, message, handler_response=None):
        command = "!welcome timeout "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                duration_string = Methods.clean(message.content[len(command):])

                try:
                    timeout_duration = TimeoutDuration.from_user_string(duration_string)
                except ValueError:
                    handler_response.add(MessageFormats.cannot_parse_timeout_string.format(duration_string))
                    return

                self.handler.state.registered_set(timeout_duration.seconds, "user_welcome_timeout_seconds", [str(message.author.id)])
                handler_response.add("Welcome message timeout duration set to {0}.".format(timeout_duration.to_user_string()))

    def _private_message_nicknames_add(self, message, handler_response=None):
        def get_possible_arguments(arguments_string):
            result = []

            target_identifier_string = arguments_string
            target_nickname = ""

            separator_index = target_identifier_string.rfind(Arguments.nickname_separator)
            while separator_index != -1:
                target_identifier_string = target_identifier_string[:separator_index]
                target_nickname = arguments_string[separator_index+len(Arguments.nickname_separator):]

                if self.handler.get_member(target_identifier_string, requester=message.author):  # If a member can be found from a substring, one of the separators must be part of the nickname
                    result.append((Methods.clean(target_identifier_string), Methods.clean(target_nickname)))

                separator_index = target_identifier_string.rfind(Arguments.nickname_separator)

            return result

        command = "!nicknames add "
        invalid_nickname_substrings = ("> ", "`", "*", "_", "~~", Arguments.nickname_separator)

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                arguments_string = Methods.clean(message.content[len(command):])

                possible_arguments = get_possible_arguments(arguments_string)

                non_empty_possible_arguments = list(filter(lambda args: args[0] and args[1], possible_arguments))
                if not non_empty_possible_arguments:
                    handler_response.add(MessageFormats.invalid_arguments.format(arguments_string))
                    return

                valid_possible_arguments = list(filter(lambda args: not any([substring in args[1] for substring in invalid_nickname_substrings]), non_empty_possible_arguments))
                if not valid_possible_arguments:
                    handler_response.add("Nicknames cannot contain the following strings of text: {0}".format(
                        ", ".join([MessageFormats.list_item.format(substring) for substring in invalid_nickname_substrings])
                        )
                    )
                    return
                if len(valid_possible_arguments) > 1:
                    handler_response.add("Conflicting nickname options: {0}".format(
                        ", ".join([MessageFormats.list_item.format(args) for args in valid_possible_arguments])
                        )
                    )
                    return

                target_identifier_string, target_nickname = valid_possible_arguments[0]
                target = self.handler.get_member(target_identifier_string, requester=message.author)
                if not target:  # Added for redundancy
                    handler_response.add(MessageFormats.cannot_find_user_identifier.format(target_identifier_string))
                    return

                nicknames = self.handler.state.registered_get("user_nicknames", [str(message.author.id)])
                for nickname in nicknames.values():
                    if Methods.clean(nickname).lower() == Methods.clean(target_nickname).lower():
                        handler_response.add("The provided nickname is already in your list: {0}".format(target_nickname))
                        return

                nicknames[str(target.id)] = target_nickname
                self.handler.state.registered_set(nicknames, "user_nicknames", [str(message.author.id)])
                handler_response.add("`{0}` has been set as your nickname for {1}.".format(target_nickname, self.handler.get_member_name(target)))