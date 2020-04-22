from discord.state import Status

from ...discordHandler import Handler
from ...classes.messageBuilder import MessageBuilder
from ...classes.eventTimeout import EventTimeout
from ...constants import KeyQueryFactories, Defaults
from ..handlerPlugin import HandlerPlugin
from .constants import MessageFormats

class Watchlist(HandlerPlugin):
    @staticmethod
    def register_paths(handler):
        handler.state.register("user_watchlist", ["user_settings", KeyQueryFactories.dynamic_key, "watchlist", "members"], [{}, {}, {}, []])
        handler.state.register("user_watchlist_alert_timeout_duration", ["user_settings", KeyQueryFactories.dynamic_key, "watchlist", "alerts", "timeout_duration"], [{}, {}, {}, {}, Defaults.timeout_duration])

    #Event method
    @staticmethod
    def user_online(before, after, handler, handler_response=None):
        responses = []

        for method in [Watchlist._watchlist_alerts]:
            method_responses = method(before, after, handler, handler_response)

            responses += method_responses if method_responses else []

        return responses

    @staticmethod
    def _watchlist_alerts(before, after, handler, handler_response=None):
        all_saved_users = [user_id_string for user_id_string in handler.state.registered_get("all_users_settings")]

        responses = []

        for user_id_string in all_saved_users:
            user_watchlist = handler.state.registered_get("user_watchlist", [user_id_string])

            if after.id in user_watchlist:
                watcher = handler.get_member(int(user_id_string))

                if watcher.status == Status.online:
                    new_timeout_duration = handler.state.registered_get("user_watchlist_alert_timeout_duration", [user_id_string])
                    timeout_triggered = handler.try_trigger_timeout("user_watchlist_alert|{0}|{1}".format(watcher.id, after.id), new_timeout_duration)

                    if timeout_triggered:
                        response = MessageBuilder([watcher])
                        response.add(MessageFormats.watchlist_user_online.format(handler.get_member_name(after, watcher)))
                    else:
                        response=None

                    responses.append(response)

        return responses
