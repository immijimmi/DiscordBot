class HandlerPlugin:
    @staticmethod
    def register_paths(handler):
        pass

    #Event method
    @staticmethod
    def on_ready(handler, handler_response=None):
        pass

    #Event method
    @staticmethod
    def process_message(message, handler, handler_response=None):
        pass

    #Event method
    @staticmethod
    def user_online(before, after, handler, handler_response=None):
        pass
