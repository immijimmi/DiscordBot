import sys
import os
import random

from ..constants import Methods, MessageFormats as HandlerMessageFormats
from ..classes.permissions import Permissions
from ..classes.messageBuilder import MessageBuilder
from .handlerPlugin import HandlerPlugin
from .constants import MessageFormats

class Meta(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self._event_methods["process_private_message"] += [
            self._private_message__reboot, self._private_message__help, self._private_message__settings, self._private_message__users,
            self._private_message__introduce
            ]

    def _private_message__reboot(self, message, handler_response=None):
        async def update_and_restart():
            if sys.platform == "linux":
                os.system("sudo git pull\nsudo reboot")
            else:
                pass  # Does not support all platforms currently

            raise SystemExit

        command = "!reboot"

        if Methods.clean(message.content).lower() == command:
            required_permissions_options = [Permissions(Permissions.level_admin, [])]
            user_permissions = Permissions(**self.handler.state.registered_get("user_permissions_data", [str(message.author.id)]))

            if user_permissions.is_permitted(*required_permissions_options):
                handler_response.add("Rebooting...")

                self.handler.add_callback(update_and_restart, to_end=True)

    def _private_message__help(self, message, handler_response=None):
        def build_command_list(commands, user_permissions):
            result = []

            for command_string in commands:
                command = commands[command_string]

                for usage in command["usage"]:
                    required_permissions_options = usage["permissions"]
                    if not user_permissions.is_permitted(*required_permissions_options):
                        continue

                    arguments_string = " ".join(["`{0}`".format(argument) for argument in usage["arguments"]])
                    result_string = "**- {1}** {2} {0} *{3}*".format(usage["visibility"], command_string, arguments_string, usage["description"])

                    result.append(result_string)

                for child_result_string in build_command_list(command["children"], user_permissions):
                    result.append("       " + child_result_string)

            return result

        command = "!help"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                user_permissions = Permissions(**self.handler.state.registered_get("user_permissions_data", [str(message.author.id)]))

                key_string = "**Command List:**" + "\n"
                key_string += "*Key: "
                key_string += ":lock: `used by messaging the bot` "
                key_string += ":unlock: `used in server and group channels` "
                key_string += ":arrows_clockwise: `can be used either way`*"

                handler_response.title = key_string
                handler_response.add("\n".join(build_command_list(MessageFormats.commands, user_permissions)))

    def _private_message__users(self, message, handler_response=None):
        command = "!users"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                required_permissions_options = [Permissions(Permissions.level_admin, [])]
                user_permissions = Permissions(**self.handler.state.registered_get("user_permissions_data", [str(message.author.id)]))

                if user_permissions.is_permitted(*required_permissions_options):
                    all_saved_users = [user_id_string for user_id_string in self.handler.state.registered_get("all_users_settings")]
                    names = [self.handler.try_get_member_name(user_id_string, requester_id=message.author.id) or user_id_string for user_id_string in all_saved_users]

                    if not names:
                        handler_response.add(MessageFormats.note__no_bot_users)
                        return

                    handler_response.title = "**User List:**"
                    handler_response.add("\n".join(["- {0}".format(name) for name in names]))
                    return

    def _private_message__introduce(self, message, handler_response=None):
        command = "!introduce "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                required_permissions_options = [Permissions(Permissions.level_admin, [])]
                user_permissions = Permissions(**self.handler.state.registered_get("user_permissions_data", [str(message.author.id)]))

                if user_permissions.is_permitted(*required_permissions_options):
                    target_identifier = Methods.clean(message.content[len(command):])

                    target = self.handler.try_get_member(target_identifier, requester_id=message.author.id)
                    if not target:
                        handler_response.add(MessageFormats.cannot_find_user__identifier.format(target_identifier))
                        return
                    elif type(target) is list:
                        handler_response.add(MessageFormats.multiple_user_matches)
                        return

                    target_name = self.handler.try_get_member_name(target.id, requester_id=message.author.id)

                    response = MessageBuilder(recipients=[target])
                    response.add(random.choice(MessageFormats.introductions__username).format(target.name) + "\n" + HandlerMessageFormats.note__help)

                    handler_response.add("Introduction sent to {0}.".format(target_name))

                    return [response]