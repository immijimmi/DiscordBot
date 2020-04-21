class HandlerPlugin:
    @staticmethod
    def register_paths(handler):
        pass
    
    @staticmethod
    def on_ready(handler, handler_response=None):
        pass

    @staticmethod
    def process_message(message, handler, handler_response=None):
        pass

    @staticmethod
    def user_online(before, after, handler, handler_response=None):
        pass
