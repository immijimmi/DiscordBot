from ...constants import Methods
from ..handlerPlugin import HandlerPlugin
from .constants import PermissionsValues

class Dadi(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self._event_methods["process_public_message"] += [self._public_message__kavica]

        self.permissions_tags += PermissionsValues.tags

    def _public_message__kavica(self, message, handler_response=None):
        command = "&kavica"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                handler_response.add(":coffee: 1,20 evra prosim")
