import sys
import os

from ...constants import Methods, Permissions
from ..handlerPlugin import HandlerPlugin
from .constants import MessageFormats

class Meta(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self.event_methods["process_private_message"] += [self._reboot, self._help_private]

    def _reboot(self, message, handler_response=None):
        async def update_and_restart():
            if sys.platform == "linux":
                os.system("sudo git pull\nsudo reboot")
            else:
                pass  # Does not support all platforms currently

        command = "!reboot"

        if Methods.sanitise_message(message.content).lower() == command:
            author_permissions_level = self.handler.state.registered_get("user_permissions_level", [str(message.author.id)])

            if author_permissions_level >= Permissions.level_admin:
                handler_response.add("Rebooting...")

                self.handler.add_callback(update_and_restart, to_end=True)

    def _help_private(self, message, handler_response=None):
        def build_command_list(commands, permissions_level=Permissions.level_none):
            result = []

            for command in commands:
                for usage in commands[command]["usage"]:
                    permissions_requirement = usage["permissions_level"]
                    if permissions_level < permissions_requirement:
                        continue

                    arguments_string = " ".join(["`{0}`".format(argument) for argument in usage["arguments"]])
                    result_string = "**- {1}** {2} {0} *{3}*".format(usage["visibility"], command, arguments_string, usage["description"])

                    result.append(result_string)

                for child_result_string in build_command_list(commands[command]["children"]):
                    result.append("       " + child_result_string)

            return result

        command = "!help"

        if handler_response is not None:
            if Methods.sanitise_message(message.content).lower() == command:
                author_permissions_level = self.handler.state.registered_get("user_permissions_level", [str(message.author.id)])

                handler_response.title = "**Command List:**" + "\n"
                handler_response.title += "*Key: "
                handler_response.title += ":lock: `used by messaging the bot` "
                handler_response.title += ":unlock: `used by messaging in the server` "
                handler_response.title += ":arrows_clockwise: `can be used either way`*" + "\n"

                handler_response.add("\n".join(build_command_list(MessageFormats.commands, permissions_level=author_permissions_level)))
