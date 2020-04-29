import abc

class HandlerPlugin(abc.ABC):
    def __init__(self, handler):
        self.handler = handler

        self._event_methods = {
            "on_ready": [],
            "process_private_message": [],
            "process_public_message": [],
            "user_online": [],
            "user_away": []
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

    def _register_paths(self):
        pass
