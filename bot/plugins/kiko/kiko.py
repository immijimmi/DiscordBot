from ...constants import Methods
from ..handlerPlugin import HandlerPlugin
from .constants import MessageFormats, PermissionsValues

class Kiko(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self._event_methods["process_public_message"] += [self._public_message__mc]

        self.permissions_tags += PermissionsValues.tags

    def _register_paths(self):
        self.handler.state.register("server_id_sanctuary", ["server_ids", "the_sanctuary"], [{}, None])
        self.handler.state.register("mc_server_ip", ["plugin_settings", "kiko", "mc_server_ip"], [{}, {}, None])

    def _public_message__mc(self, message, handler_response=None):
        command = "!mc"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                server_id = self.handler.state.registered_get("server_id_sanctuary")

                if str(message.channel.guild.id) == server_id:
                    mc_server_ip = self.handler.state.registered_get("mc_server_ip")

                    if mc_server_ip:
                        handler_response.add(MessageFormats.mc_setup__server_ip.format(mc_server_ip))