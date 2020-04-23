from discord.state import Status

from ...discordHandler import Handler
from ...classes.messageBuilder import MessageBuilder
from ...classes.eventTimeout import EventTimeout
from ...constants import KeyQueryFactories, Defaults
from ..handlerPlugin import HandlerPlugin
from .constants import MessageFormats, SymbolLookup

class Watchlist(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self.event_methods["user_online"] += [self._welcome_message, self._watchlist_alerts]

    def _welcome_message(self, before, after, handler_response=None):
        if handler_response is not None:
            user_watchlist = self.handler.state.registered_get("user_watchlist", [str(after.id)])

            if user_watchlist:
                message = MessageFormats.watchlist_welcome_title + "\n"

                user_statuses = {}

                for user_id in user_watchlist:
                    user = self.handler.get_member(user_id)

                    if user:
                        user_name = self.handler.get_member_name(user, requester=after)
                        user_status_message = SymbolLookup.status[user.status] + " " + user_name + "\n"
                        
                        user_statuses[user.status] = user_statuses.get(user.status, []) + [user_status_message]

                for status in MessageFormats.status_order:
                    message += "".join(user_statuses.get(status, []))

                handler_response.add(message)

    def _watchlist_alerts(self, before, after, handler_response=None):
        all_saved_users = [user_id_string for user_id_string in self.handler.state.registered_get("all_users_settings")]

        responses = []

        for user_id_string in all_saved_users:
            user_watchlist = self.handler.state.registered_get("user_watchlist", [user_id_string])

            if after.id in user_watchlist:
                watcher = self.handler.get_member(int(user_id_string))
                setting_enabled = self.handler.state.registered_get("user_watchlist_alert_enabled", [user_id_string])

                if watcher and setting_enabled and (watcher.status == Status.online):
                    new_timeout_duration = self.handler.state.registered_get("user_watchlist_alert_timeout_duration", [user_id_string])
                    timeout_triggered = self.handler.try_trigger_timeout("user_watchlist_alert|{0}|{1}".format(watcher.id, after.id), new_timeout_duration)

                    if timeout_triggered:
                        response = MessageBuilder([watcher])
                        response.add(MessageFormats.watchlist_user_online.format(self.handler.get_member_name(after, watcher)))
                    else:
                        response=None

                    responses.append(response)

        return responses

    def _register_paths(self):
        self.handler.state.register("user_watchlist", ["user_settings", KeyQueryFactories.dynamic_key, "watchlist", "members"], [{}, {}, {}, []])
        self.handler.state.register(
            "user_watchlist_alert_timeout_duration",
            ["user_settings", KeyQueryFactories.dynamic_key, "watchlist", "alerts", "timeout_duration"],
            [{}, {}, {}, {}, Defaults.timeout_duration]
            )
        self.handler.state.register(
            "user_watchlist_alert_enabled",
            ["user_settings", KeyQueryFactories.dynamic_key, "watchlist", "alerts", "enabled"],
            [{}, {}, {}, {}, True]
            )
