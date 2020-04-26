from discord.state import Status

from ...classes.messageBuilder import MessageBuilder
from ...classes.eventTimeout import EventTimeout
from ...constants import KeyQueryFactories, Defaults, Methods, MessageFormats as HandlerMessageFormats
from ..handlerPlugin import HandlerPlugin
from .constants import MessageFormats, SymbolLookup, EventKeys

class Watchlist(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self._watchlist_alerts = {}

        self.event_methods["user_online"] += [self._welcome_message, self._watchlist_alert]
        self.event_methods["process_private_message"] += [self._watchlist, self._watchlist_add, self._watchlist_remove]
        self.event_methods["user_away"] += [self._watchlist_remove_alert]

    def _welcome_message(self, before, after, handler_response=None):
        if handler_response is not None:
            user_watchlist = self.handler.state.registered_get("user_watchlist", [str(after.id)])

            if user_watchlist:
                message = MessageFormats.watchlist_title + "\n"

                target_statuses = {}

                for target_id in user_watchlist:
                    target = self.handler.get_member(target_id)

                    if target:
                        target_name = self.handler.get_member_name(target, requester=after)
                        target_status_message = SymbolLookup.status[target.status] + " " + target_name + "\n"
                        
                        target_statuses[target.status] = target_statuses.get(target.status, []) + [target_status_message]

                if target_statuses:  # If there is at least one recognised user in the watchlist
                    for status in MessageFormats.status_order:
                        message += "".join(target_statuses.get(status, []))

                    handler_response.add(message)

    def _watchlist_alert(self, before, after, handler_response=None):
        all_saved_users = [user_id_string for user_id_string in self.handler.state.registered_get("all_users_settings")]

        responses = []

        for watcher_id_string in all_saved_users:
            watcher_watchlist = self.handler.state.registered_get("user_watchlist", [watcher_id_string])

            if after.id in watcher_watchlist:
                watcher = self.handler.get_member(int(watcher_id_string))
                setting_enabled = self.handler.state.registered_get("user_watchlist_alert_enabled", [watcher_id_string])

                if watcher and setting_enabled and (watcher.status == Status.online):
                    new_timeout_duration = self.handler.state.registered_get("user_watchlist_alert_timeout_duration", [watcher_id_string])
                    alert_key = EventKeys.watchlist_alerts.format(watcher.id, after.id)
                    timeout_triggered = self.handler.try_trigger_timeout(alert_key, new_timeout_duration)

                    if timeout_triggered:
                        def track_alert_message(discord_message):
                            self._watchlist_alerts[alert_key] = self._watchlist_alerts.get(alert_key, []) + [discord_message]

                        response = MessageBuilder([watcher])
                        response.add(MessageFormats.watchlist_user_online.format(self.handler.get_member_name(after, watcher)))
                        response.add_callback(track_alert_message)
                    else:
                        response=None

                    responses.append(response)

        return responses

    def _watchlist_remove_alert(self, before, after, handler_response=None):
        all_saved_users = [user_id_string for user_id_string in self.handler.state.registered_get("all_users_settings")]

        for watcher_id_string in all_saved_users:
            watcher_watchlist = self.handler.state.registered_get("user_watchlist", [watcher_id_string])

            if after.id in watcher_watchlist:
                watcher = self.handler.get_member(int(watcher_id_string))

                if watcher:
                    alert_key = EventKeys.watchlist_alerts.format(watcher.id, after.id)
                    alerts = self._watchlist_alerts.get(alert_key, [])
                    self._watchlist_alerts[alert_key] = []

                    async def delete_alert_messages():
                        for discord_message in alerts:
                            await discord_message.delete()

                    self.handler.add_callback(delete_alert_messages)

    def _watchlist(self, message, handler_response=None):
        command = "!watchlist"

        if handler_response is not None:
            if Methods.sanitise_message(message.content).lower() == command:
                watchlist = self.handler.state.registered_get("user_watchlist", [str(message.author.id)])
                watchlist_names = []

                for target_id in watchlist:
                    target = self.handler.get_member(target_id)
                    target_name = self.handler.get_member_name(target, requester=message.author) if target else str(target_id)
                    watchlist_names.append(target_name)

                if watchlist_names:
                    message = MessageFormats.watchlist_title + "\n"
                    message += "\n".join(watchlist_names)

                    handler_response.add(message)

                else:
                    handler_response.add("Your watchlist is empty.")

    def _watchlist_add(self, message, handler_response=None):
        command = "!watchlist add "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                target_identifier = Methods.sanitise_message(message.content[len(command):])
                target = self.handler.get_member(target_identifier, requester=message.author)

                if target:
                    target_name = self.handler.get_member_name(target, requester=message.author)
                    watchlist = self.handler.state.registered_get("user_watchlist", [str(message.author.id)])

                    if target.id in watchlist:
                        handler_response.add("{0} is already in your watchlist.".format(target_name))

                    else:
                        self.handler.state.registered_set(watchlist + [target.id], "user_watchlist", [str(message.author.id)])

                        handler_response.add("{0} has been added to your watchlist.".format(target_name))

                else:
                    handler_response.add(HandlerMessageFormats.cannot_find_user_identifier.format(target_identifier))

    def _watchlist_remove(self, message, handler_response=None):
        command = "!watchlist remove "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                target_identifier = Methods.sanitise_message(message.content[len(command):])

                target = self.handler.get_member(target_identifier, requester=message.author)
                watchlist = self.handler.state.registered_get("user_watchlist", [str(message.author.id)])

                if target:
                    target_name = self.handler.get_member_name(target, requester=message.author)

                    if target.id in watchlist:
                        self.handler.state.registered_set(list(filter(lambda user_id: user_id != target.id, watchlist)), "user_watchlist", [str(message.author.id)])

                        handler_response.add("{0} has been removed from your watchlist.".format(target_name))

                    else:
                        handler_response.add("{0} is not in your watchlist.".format(target_name))

                elif target_identifier in [str(target_id) for target_id in watchlist]:
                    target_id = int(target_identifier)

                    self.handler.state.registered_set(list(filter(lambda id: id != target_id, watchlist)), "user_watchlist", [str(message.author.id)])

                    handler_response.add("{0} has been removed from your watchlist.".format(target_identifier))

                else:
                    handler_response.add(HandlerMessageFormats.cannot_find_user_identifier.format(target_identifier))

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
