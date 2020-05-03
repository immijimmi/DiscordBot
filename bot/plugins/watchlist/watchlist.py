from discord.state import Status

from ...classes.messageBuilder import MessageBuilder
from ...classes.eventTimeout import EventTimeout
from ...classes.timeoutDuration import TimeoutDuration
from ...constants import KeyQueryFactories, Defaults, Methods
from ..constants import MessageFormats as PluginMessageFormats
from ..handlerPlugin import HandlerPlugin
from .constants import MessageFormats, SymbolLookup, EventKeys

class Watchlist(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self._event_methods["user_online"] += [self._online_welcome_watchlist, self._online_watchlist_alert]
        self._event_methods["process_private_message"] += [
            self._private_message_watchlist, self._private_message_watchlist_toggle, self._private_message_watchlist_timeout_change,
            self._private_message_watchlist_add, self._private_message_watchlist_remove
            ]

    def _register_paths(self):
        self.handler.state.register("user_watchlist", ["user_settings", KeyQueryFactories.dynamic_key, "watchlist", "members"], [{}, {}, {}, []])
        self.handler.state.register(
            "user_watchlist_alert_timeout_seconds",
            ["user_settings", KeyQueryFactories.dynamic_key, "watchlist", "alerts", "timeout_duration"],
            [{}, {}, {}, {}, Defaults.timeout_duration.seconds]
            )
        self.handler.state.register(
            "user_watchlist_alerts_enabled",
            ["user_settings", KeyQueryFactories.dynamic_key, "watchlist", "alerts", "enabled"],
            [{}, {}, {}, {}, True]
            )

    def _online_welcome_watchlist(self, before, after, handler_response=None):
        if handler_response is not None:
            watchlist_statuses = self.__user_watchlist_status_strings(after)
            
            if watchlist_statuses:
                handler_response.add(MessageFormats.watchlist_title_private + "\n" + "\n".join(watchlist_statuses))

    def _online_watchlist_alert(self, before, after, handler_response=None):
        all_saved_users = [user_id_string for user_id_string in self.handler.state.registered_get("all_users_settings")]

        responses = []

        for watcher_id_string in all_saved_users:
            watcher_watchlist = self.handler.state.registered_get("user_watchlist", [watcher_id_string])

            if after.id in watcher_watchlist:
                watcher = self.handler.get_member(int(watcher_id_string))
                setting_enabled = self.handler.state.registered_get("user_watchlist_alerts_enabled", [watcher_id_string])

                if watcher and (watcher.status == Status.online) and setting_enabled:
                    new_timeout_duration = TimeoutDuration(self.handler.state.registered_get("user_watchlist_alert_timeout_seconds", [watcher_id_string]))
                    alert_key = EventKeys.watchlist_alerts.format(watcher.id, after.id)
                    timeout_triggered = self.handler.try_trigger_timeout(alert_key, new_timeout_duration)

                    if timeout_triggered:
                        response = MessageBuilder([watcher])
                        response.add(
                            MessageFormats.watchlist_user_online.format(self.handler.get_member_name(after, requester=watcher))
                        )
                    else:
                        response=None

                    responses.append(response)

        return responses

    def _private_message_watchlist(self, message, handler_response=None):
        command = "!watchlist"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                watchlist_statuses = self.__user_watchlist_status_strings(message.author)

                if watchlist_statuses:
                    handler_response.add(MessageFormats.watchlist_title_private + "\n" + "\n".join(watchlist_statuses) + "\n")
                else:
                    handler_response.add("Your watchlist is empty." + "\n")

                settings_string = "**Watchlist Settings:**" + "\n"

                watchlist_status = "enabled" if self.handler.state.registered_get("user_watchlist_alerts_enabled", [str(message.author.id)]) else "disabled"
                settings_string += "status: " + "`" + watchlist_status + "`" + "\n"

                timeout_duration = TimeoutDuration(self.handler.state.registered_get("user_watchlist_alert_timeout_seconds", [str(message.author.id)]))
                settings_string += "timeout duration: " + "`" + timeout_duration.to_user_string() + "`"

                handler_response.add(settings_string)

    def _private_message_watchlist_toggle(self, message, handler_response=None):
        command = "!watchlist "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                toggle_string = Methods.clean(message.content[len(command):])

                if toggle_string.lower() in PluginMessageFormats.toggle_on_strings:
                    setting_enabled = True
                elif toggle_string.lower() in PluginMessageFormats.toggle_off_strings:
                    setting_enabled = False
                elif toggle_string.lower() in PluginMessageFormats.toggle_change_strings:
                    setting_enabled = not self.handler.state.registered_get("user_watchlist_alerts_enabled", [str(message.author.id)])
                else:
                    return

                self.handler.state.registered_set(setting_enabled, "user_watchlist_alerts_enabled", [str(message.author.id)])
                handler_response.add("Watchlist alerts {0}.".format("enabled" if setting_enabled else "disabled"))

    def _private_message_watchlist_timeout_change(self, message, handler_response=None):
        command = "!watchlist timeout "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                duration_string = Methods.clean(message.content[len(command):])

                try:
                    timeout_duration = TimeoutDuration.from_user_string(duration_string)
                except ValueError:
                    handler_response.add(PluginMessageFormats.cannot_parse_timeout_string.format(duration_string))
                    return

                self.handler.state.registered_set(timeout_duration.seconds, "user_watchlist_alert_timeout_seconds", [str(message.author.id)])
                handler_response.add("Watchlist timeout duration set to {0}.".format(timeout_duration.to_user_string()))

    def _private_message_watchlist_add(self, message, handler_response=None):
        command = "!watchlist add "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                target_identifier = Methods.clean(message.content[len(command):])
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
                    handler_response.add(PluginMessageFormats.cannot_find_user_identifier.format(target_identifier))

    def _private_message_watchlist_remove(self, message, handler_response=None):
        command = "!watchlist remove "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                target_identifier = Methods.clean(message.content[len(command):])
                target = self.handler.get_member(target_identifier, requester=message.author)
                
                watchlist = self.handler.state.registered_get("user_watchlist", [str(message.author.id)])

                if target:
                    target_name = self.handler.get_member_name(target, requester=message.author)

                    if target.id in watchlist:
                        self.handler.state.registered_set(list(filter(lambda user_id: user_id != target.id, watchlist)), "user_watchlist", [str(message.author.id)])
                        handler_response.add(MessageFormats.watchlist_user_removed.format(target_name))

                    else:
                        handler_response.add("{0} is not in your watchlist.".format(target_name))

                elif target_identifier in [str(target_id) for target_id in watchlist]:
                    target_id = int(target_identifier)

                    self.handler.state.registered_set(list(filter(lambda id: id != target_id, watchlist)), "user_watchlist", [str(message.author.id)])
                    handler_response.add(MessageFormats.watchlist_user_removed.format(target_identifier))

                else:
                    handler_response.add(PluginMessageFormats.cannot_find_user_identifier.format(target_identifier))

    def __user_watchlist_status_strings(self, user):
        watchlist = self.handler.state.registered_get("user_watchlist", [str(user.id)])
        result = []

        if watchlist:
            target_statuses = {}

            for target_id in watchlist:
                target = self.handler.get_member(target_id)

                if target:
                    target_name = self.handler.get_member_name(target, requester=user)
                    target_status_message = SymbolLookup.status[target.status] + " " + target_name
                    
                    target_statuses[target.status] = target_statuses.get(target.status, []) + [target_status_message]

                    if target.status == Status.online:  # Trigger online alert timeouts for the recipient, for any users that this message will show as online
                        new_timeout_duration = TimeoutDuration(self.handler.state.registered_get("user_watchlist_alert_timeout_seconds", [str(user.id)]))
                        alert_key = EventKeys.watchlist_alerts.format(user.id, target.id)
                        self.handler.try_trigger_timeout(alert_key, new_timeout_duration)

            if target_statuses:  # If there is at least one recognised user in the watchlist
                for status in MessageFormats.status_order:
                    result += target_statuses.get(status, [])

                return result