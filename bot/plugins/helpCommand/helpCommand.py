from ..handlerPlugin import HandlerPlugin

class HelpCommand(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self.event_methods["process_private_message"] += [self._help_private]

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
            if Methods.sanitise_message(message.content).lower() == command:
                handler_response.title = "**Command List:**" + "\n"
                handler_response.title += "*Key: "
                handler_response.title += ":lock: `used by messaging the bot` "
                handler_response.title += ":unlock: `used by messaging in the server` "
                handler_response.title += ":arrows_clockwise: `can be used either way`*" + "\n"

                handler_response.add("\n".join(build_command_list(MessageFormats.commands)))
