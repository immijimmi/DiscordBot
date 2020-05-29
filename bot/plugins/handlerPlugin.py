import abc
from functools import reduce

from ..classes.permissions import Permissions
from ..constants import Methods
from .constants import MessageFormats

class HandlerPlugin(abc.ABC):
    def __init__(self, handler):
        self.handler = handler

        self._event_methods = {
            "on_ready": [],
            "process_private_message": [self._private_message__settings, self._private_message__settings_user],
            "process_public_message": [],
            "user_online": [],
            "user_away": [],
            }

        self._meta_methods = {
            "settings": []
        }

        self.permissions_tags = []

        self._register_paths()

    def on_ready(self, handler_response=None):
        """
        Event Method
        """
        responses = []

        for method in self._event_methods["on_ready"]:
            method_responses = method(handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def process_private_message(self, message, handler_response=None):
        """
        Event Method
        """
        responses = []

        for method in self._event_methods["process_private_message"]:
            method_responses = method(message, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def process_public_message(self, message, handler_response=None):
        """
        Event Method
        """
        responses = []

        for method in self._event_methods["process_public_message"]:
            method_responses = method(message, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def user_online(self, before, after, handler_response=None):
        """
        Event Method
        """
        responses = []

        for method in self._event_methods["user_online"]:
            method_responses = method(before, after, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def user_away(self, before, after, handler_response=None):
        """
        Event Method
        """
        responses = []

        for method in self._event_methods["user_away"]:
            method_responses = method(before, after, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def _get_all_permissions_tags(self):
        return list(Permissions.tags) + list(reduce(lambda a,b: a+b, (list(plugin.permissions_tags) for plugin in self.handler.plugins)))

    def _private_message__settings(self, message, handler_response=None):
        command = "!settings"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                responses = []

                for method in self._meta_methods["settings"]:
                    method_responses = method(message.author.id, handler_response)

                    responses += method_responses if method_responses else []

                return responses

    def _private_message__settings_user(self, message, handler_response=None):
        command = "!settings "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                required_permissions_options = [Permissions(Permissions.levels["admin"], [])]
                user_permissions = Permissions(**self.handler.state.registered_get("user_permissions_data", [str(message.author.id)]))

                if user_permissions.is_permitted(*required_permissions_options):
                    target_identifier = Methods.clean(message.content[len(command):])

                    all_saved_users = [user_id_string for user_id_string in self.handler.state.registered_get("all_users_settings")]

                    target_id = self.handler.try_get_member_id(target_identifier, requester_id=message.author.id)
                    if not target_id:
                        if not handler_response:
                            handler_response.add(MessageFormats.cannot_find_user__identifier.format(target_identifier))
                        return
                    elif type(target_id) is list:
                        if not handler_response:
                            handler_response.add(MessageFormats.multiple_user_matches)
                        return

                    target_name = self.handler.try_get_member_name(target_id, requester_id=message.author.id) or target_id

                    if str(target_id) not in all_saved_users:
                        if not handler_response:
                            handler_response.add("No settings found for {0}.".format(target_name))
                        return

                    handler_response.title = "**Settings for User:** {0}".format(target_name)

                    responses = []

                    for method in self._meta_methods["settings"]:
                        method_responses = method(target_id, handler_response)

                        responses += method_responses if method_responses else []

                    return responses

    def _register_paths(self):
        pass