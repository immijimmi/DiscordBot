from ..classes.timeoutDuration import TimeoutDuration
from ..constants import Methods, MessageFormats
from .handlerPlugin import HandlerPlugin

class Essentials(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self._event_methods["process_private_message"] += [self._welcome, self._welcome_toggle, self._welcome_timeout_change]

    def _welcome(self, message, handler_response=None):
        command = "!welcome"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                settings_string = "**Welcome Message Settings:**" + "\n"

                welcome_status = "enabled" if self.handler.state.registered_get("user_welcome_enabled", [str(message.author.id)]) else "disabled"
                settings_string += "status: " + "`" + welcome_status + "`" + "\n"

                timeout_duration = TimeoutDuration(self.handler.state.registered_get("user_welcome_timeout_seconds", [str(message.author.id)]))
                settings_string += "timeout duration: " + "`" + timeout_duration.to_user_string() + "`"

                handler_response.add(settings_string)

    def _welcome_toggle(self, message, handler_response=None):
        command = "!welcome "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                toggle_string = Methods.clean(message.content[len(command):]).lower()

                if toggle_string in MessageFormats.toggle_on_strings:
                    setting_enabled = True
                elif toggle_string in MessageFormats.toggle_off_strings:
                    setting_enabled = False
                elif toggle_string in MessageFormats.toggle_change_strings:
                    setting_enabled = not self.handler.state.registered_get("user_welcome_enabled", [str(message.author.id)])
                else:
                    return

                self.handler.state.registered_set(setting_enabled, "user_welcome_enabled", [str(message.author.id)])
                handler_response.add("Welcome messages {0}.".format("enabled" if setting_enabled else "disabled"))

    def _welcome_timeout_change(self, message, handler_response=None):
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