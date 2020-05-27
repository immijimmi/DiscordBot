from ..classes.timeoutDuration import TimeoutDuration
from ..classes.permissions import Permissions
from ..constants import Methods, MessageFormats as HandlerMessageFormats
from .constants import MessageFormats, Arguments
from .handlerPlugin import HandlerPlugin

class Essentials(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self._event_methods["process_private_message"] += [
            self._private_message__welcome, self._private_message__welcome_toggle, self._private_message__welcome_timeout_change,
            self._private_message__nicknames, self._private_message__nicknames_add, self._private_message__nicknames_remove
            ]

        self._meta_methods["settings"] += [self._settings__welcome, self._settings__nicknames]

    def _private_message__welcome(self, message, handler_response=None):
        command = "!welcome"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                return self._settings__welcome(message.author.id, handler_response)

    def _settings__welcome(self, user_id, handler_response):
        settings_string = "**Welcome Message Settings:**" + "\n"

        welcome_status = "enabled" if self.handler.state.registered_get("user_welcome_enabled", [str(user_id)]) else "disabled"
        settings_string += "status: " + "`" + welcome_status + "`" + "\n"

        timeout_duration = TimeoutDuration(self.handler.state.registered_get("user_welcome_timeout_seconds", [str(user_id)]))
        settings_string += "timeout duration: " + "`" + timeout_duration.to_user_string() + "`"

        handler_response.add(settings_string)

    def _private_message__welcome_toggle(self, message, handler_response=None):
        command = "!welcome "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                toggle_string = Methods.clean(message.content[len(command):])

                if toggle_string.lower() in Arguments.toggle_on_strings:
                    setting_enabled = True
                elif toggle_string.lower() in Arguments.toggle_off_strings:
                    setting_enabled = False
                elif toggle_string.lower() in Arguments.toggle_change_strings:
                    setting_enabled = not self.handler.state.registered_get("user_welcome_enabled", [str(message.author.id)])
                else:
                    return

                self.handler.state.registered_set(setting_enabled, "user_welcome_enabled", [str(message.author.id)])
                handler_response.add("Welcome messages {0}.".format("enabled" if setting_enabled else "disabled"))

    def _private_message__welcome_timeout_change(self, message, handler_response=None):
        command = "!welcome timeout "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                duration_string = Methods.clean(message.content[len(command):])

                try:
                    timeout_duration = TimeoutDuration.from_user_string(duration_string)
                except ValueError:
                    handler_response.add(MessageFormats.cannot_parse__timeout_string.format(duration_string))
                    return

                self.handler.state.registered_set(timeout_duration.seconds, "user_welcome_timeout_seconds", [str(message.author.id)])
                handler_response.add("Welcome message timeout duration set to {0}.".format(timeout_duration.to_user_string()))

    def _private_message__nicknames(self, message, handler_response=None):
        command = "!nicknames"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                return self._settings__nicknames(message.author.id, handler_response)

    def _settings__nicknames(self, user_id, handler_response):
        nicknames = self.handler.state.registered_get("user_nicknames", [str(user_id)])

        nickname_lines = []
        for target_id_string, target_nickname in nicknames.items():
            target_discord_name = self.handler.try_get_member_name(target_id_string, requester_id=None) or MessageFormats.placeholder__cannot_find_user

            nickname_lines.append("- {0} ({1})".format(Methods.clean(target_nickname), target_discord_name))

        if nickname_lines:
            nicknames_string = "**Nicknames:**" + "\n"
            nicknames_string += "\n".join(nickname_lines)
        else:
            nicknames_string = MessageFormats.note__no_nicknames

        handler_response.add(nicknames_string)

    def _private_message__nicknames_add(self, message, handler_response=None):
        def get_possible_arguments(arguments_string):
            result = []

            target_identifier_string = arguments_string
            target_nickname = ""

            separator_index = target_identifier_string.rfind(Arguments.nickname_separator)
            while separator_index != -1:
                target_identifier_string = target_identifier_string[:separator_index]
                target_nickname = arguments_string[separator_index+len(Arguments.nickname_separator):]

                if self.handler.try_get_member(target_identifier_string, requester_id=message.author.id):  # If a member can be found from a substring, one of the separators must be part of the nickname
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
                    if Arguments.nickname_separator in arguments_string:
                        handler_response.add(MessageFormats.cannot_find_user)
                        return
                    else:
                        handler_response.add(MessageFormats.invalid__arguments.format(arguments_string))
                        return

                valid_possible_arguments = list(filter(lambda args: not any([substring in args[1] for substring in invalid_nickname_substrings]), non_empty_possible_arguments))
                if not valid_possible_arguments:
                    handler_response.add("Nicknames cannot contain the following strings of text: {0}".format(
                        ", ".join([HandlerMessageFormats.format__list_item.format(substring) for substring in invalid_nickname_substrings])
                        )
                    )
                    return
                if len(valid_possible_arguments) > 1:
                    handler_response.add("Conflicting nickname options: {0}".format(
                        ", ".join([HandlerMessageFormats.format__list_item.format(args) for args in valid_possible_arguments])
                        )
                    )
                    return

                target_identifier_string, target_nickname = valid_possible_arguments[0]
                target = self.handler.try_get_member(target_identifier_string, requester_id=message.author.id)
                if not target:  # Added for redundancy
                    handler_response.add(MessageFormats.cannot_find_user__identifier.format(target_identifier_string))
                    return
                elif type(target) is list:
                    handler_response.add(MessageFormats.multiple_user_matches)
                    return

                nicknames = self.handler.state.registered_get("user_nicknames", [str(message.author.id)])
                for nickname in nicknames.values():
                    if Methods.clean(nickname).lower() == target_nickname.lower():
                        handler_response.add("The provided nickname is already in your list: {0}".format(target_nickname))
                        return

                nicknames[str(target.id)] = target_nickname
                self.handler.state.registered_set(nicknames, "user_nicknames", [str(message.author.id)])
                handler_response.add("{0} has been set as your nickname for {1}.".format(target_nickname, self.handler.try_get_member_name(target.id, requester_id=None)))

    def _private_message__nicknames_remove(self, message, handler_response=None):
        command = "!nicknames remove "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                target_identifier = Methods.clean(message.content[len(command):])

                target_id = self.handler.try_get_member_id(target_identifier, requester_id=message.author.id)
                if not target_id:
                    handler_response.add(MessageFormats.cannot_find_nickname__identifier.format(target_identifier))
                    return
                elif type(target_id) is list:
                    handler_response.add(MessageFormats.multiple_user_matches)
                    return

                nicknames = self.handler.state.registered_get("user_nicknames", [str(message.author.id)])
                if str(target_id) in nicknames:
                    target_discord_name = self.handler.try_get_member_name(target_id, requester_id=None)
                    nickname = nicknames[str(target_id)]

                    del nicknames[str(target_id)]
                    self.handler.state.registered_set(nicknames, "user_nicknames", [str(message.author.id)])

                    handler_response.add(MessageFormats.nickname_deleted__name_nickname.format(target_discord_name, nickname))
                    return

                else:
                    handler_response.add(MessageFormats.cannot_find_nickname__identifier.format(target_identifier))
                    return
    
    def __is_permissions_tag(self, tag):
        return tag in Permissions.tags or any(tag in plugin.permissions_tags for plugin in self.handler.plugins)