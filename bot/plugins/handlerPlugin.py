class HandlerPlugin:
    def __init__(self, handler):
        self.handler = handler

        self.event_methods = {"on_ready": [], "process_message": [], "user_online": []}

        self._register_paths()

    def on_ready(self, handler_response=None):
        responses = []

        for method in event_methods["on_ready"]:
            method_responses = method(handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def process_message(self, message, handler_response=None):
        responses = []

        for method in event_methods["process_message"]:
            method_responses = method(message, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def user_online(self, before, after, handler_response=None):
        responses = []

        for method in event_methods["user_online"]:
            method_responses = method(before, after, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def _register_paths(self):
        pass