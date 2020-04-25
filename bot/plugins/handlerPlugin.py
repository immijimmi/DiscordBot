from .constants import MessageFormats

class HandlerPlugin:
    def __init__(self, handler):
        self.handler = handler

        self.event_methods = {"on_ready": [], "process_private_message": [self._help_private], "process_public_message": [], "user_online": []}

        self._register_paths()

    def on_ready(self, handler_response=None):
        responses = []

        for method in self.event_methods["on_ready"]:
            method_responses = method(handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def process_private_message(self, message, handler_response=None):
        responses = []

        for method in self.event_methods["process_private_message"]:
            method_responses = method(message, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def process_public_message(self, message, handler_response=None):
        responses = []

        for method in self.event_methods["process_public_message"]:
            method_responses = method(message, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def user_online(self, before, after, handler_response=None):
        responses = []

        for method in self.event_methods["user_online"]:
            method_responses = method(before, after, handler_response=handler_response)

            responses += method_responses if method_responses else []

        return responses

    def _help_private(self, message, handler_response=None):
        def build_command_list(commands):
            result = []

            for command in commands:
                for usage in commands[command]["usage"]:
                    arguments_string = " ".join(["`{0}`".format(argument) for argument in usage["arguments"]])
                    result_string = "**- {1}** {2} {0} *{3}*".format(usage["visibility"], command, arguments_string, usage["description"])

                    result.append(result_string)

                for child_result_string in build_command_list(commands[command]["children"]):
                    result.append("       " + child_result_string)

            return result

        command = "!help"

        if handler_response is not None:
            if message.content.lower().strip() == command:
                handler_response.title = "**Command List:**" + "\n"
                handler_response.title += "*Key: "
                handler_response.title += ":lock: `used by messaging the bot` "
                handler_response.title += ":unlock: `used by messaging in the server` "
                handler_response.title += ":arrows_clockwise: `can be used either way`*" + "\n"

                handler_response.add("\n".join(build_command_list(MessageFormats.commands)))

    def _register_paths(self):
        pass
