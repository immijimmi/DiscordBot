class HandlerPlugin:
    def __init__(self, handler):
        self.handler = handler

        self._register_paths()

    #Event method
    def on_ready(self, handler_response=None):
        pass

    #Event method
    def process_message(self, message, handler_response=None):
        pass

    #Event method
    def user_online(self, before, after, handler_response=None):
        pass

    def _register_paths(self):
        pass
