import abc

from ..constants import Methods

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

        self._register_paths()

    def on_ready(self, handler_response=None):
        responses = []

        for method in self._event_methods["on_ready"]:
            method_responses = method(handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def process_private_message(self, message, handler_response=None):
        responses = []

        for method in self._event_methods["process_private_message"]:
            method_responses = method(message, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def process_public_message(self, message, handler_response=None):
        responses = []

        for method in self._event_methods["process_public_message"]:
            method_responses = method(message, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def user_online(self, before, after, handler_response=None):
        responses = []

        for method in self._event_methods["user_online"]:
            method_responses = method(before, after, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def user_away(self, before, after, handler_response=None):
        responses = []

        for method in self._event_methods["user_away"]:
            method_responses = method(before, after, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

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
        pass

    def _register_paths(self):
        pass
