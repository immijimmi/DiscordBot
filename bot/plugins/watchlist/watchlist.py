from discord.state import Status

from ...classes.messageBuilder import MessageBuilder
from ...classes.eventTimeout import EventTimeout
from ...classes.timeoutDuration import TimeoutDuration
from ...constants import KeyQueryFactories, Defaults, Methods
from ..constants import MessageFormats as PluginMessageFormats, SymbolLookup, Arguments
from ..handlerPlugin import HandlerPlugin
from .constants import MessageFormats, EventKeys

class Watchlist(HandlerPlugin):
    def __init__(self, handler):
        super().__init__(handler)

        self._event_methods["user_online"] += [self._welcome__watchlist, self._online__watchlist_alert]
        self._event_methods["process_private_message"] += [
            self._private_message__watchlist, self._private_message__watchlist_toggle, self._private_message__watchlist_timeout_change,
            self._private_message__watchlist_add, self._private_message__watchlist_remove
            ]

        self._meta_methods["settings"] += [self._settings__watchlist]

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

    def _welcome__watchlist(self, before, after, handler_response=None):
        if handler_response is not None:
            watchlist_statuses = self.__user_watchlist_status_strings(after.id)
            
            if watchlist_statuses:
                handler_response.add(MessageFormats.title__watchlist_private + "\n" + "\n".join(watchlist_statuses))

    def _online__watchlist_alert(self, before, after, handler_response=None):
        all_saved_users = [user_id_string for user_id_string in self.handler.state.registered_get("all_users_settings")]

        responses = []

        for watcher_id_string in all_saved_users:
            watcher_watchlist = self.handler.state.registered_get("user_watchlist", [watcher_id_string])

            if after.id in watcher_watchlist:
                watcher = self.handler.try_get_member(int(watcher_id_string))
                setting_enabled = self.handler.state.registered_get("user_watchlist_alerts_enabled", [watcher_id_string])

                if watcher and (watcher.status == Status.online) and setting_enabled:
                    new_timeout_duration = TimeoutDuration(self.handler.state.registered_get("user_watchlist_alert_timeout_seconds", [watcher_id_string]))
                    alert_key = EventKeys.watchlist_alerts.format(watcher.id, after.id)
                    timeout_triggered = self.handler.try_trigger_timeout(alert_key, new_timeout_duration)

                    if timeout_triggered:
                        response = MessageBuilder([watcher])
                        response.add(
                            MessageFormats.watchlist_user_online__name.format(self.handler.get_member_name(after, requester_id=watcher.id))
                        )
                    else:
                        response=None

                    responses.append(response)

        return responses

    def _private_message__watchlist(self, message, handler_response=None):
        command = "!watchlist"

        if handler_response is not None:
            if Methods.clean(message.content).lower() == command:
                return self._settings__watchlist(message.author, handler_response)

    def _settings__watchlist(self, user_id, handler_response):
        watchlist_statuses = self.__user_watchlist_status_strings(user_id)

        if watchlist_statuses:
            handler_response.add(MessageFormats.title__watchlist_private + "\n" + "\n".join(watchlist_statuses))
        else:
            handler_response.add("Your watchlist is empty.")

        settings_string = "**Watchlist Settings:**" + "\n"

        watchlist_status = "enabled" if self.handler.state.registered_get("user_watchlist_alerts_enabled", [str(user_id)]) else "disabled"
        settings_string += "status: `{0}`\n".format(watchlist_status)

        timeout_duration = TimeoutDuration(self.handler.state.registered_get("user_watchlist_alert_timeout_seconds", [str(user_id)]))
        settings_string += "timeout duration: `{0}`".format(timeout_duration.to_user_string())

        handler_response.add(settings_string)

    def _private_message__watchlist_toggle(self, message, handler_response=None):
        command = "!watchlist "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                toggle_string = Methods.clean(message.content[len(command):])

                if toggle_string.lower() in Arguments.toggle_on_strings:
                    setting_enabled = True
                elif toggle_string.lower() in Arguments.toggle_off_strings:
                    setting_enabled = False
                elif toggle_string.lower() in Arguments.toggle_change_strings:
                    setting_enabled = not self.handler.state.registered_get("user_watchlist_alerts_enabled", [str(message.author.id)])
                else:
                    return

                self.handler.state.registered_set(setting_enabled, "user_watchlist_alerts_enabled", [str(message.author.id)])
                handler_response.add("Watchlist alerts {0}.".format("enabled" if setting_enabled else "disabled"))

    def _private_message__watchlist_timeout_change(self, message, handler_response=None):
        command = "!watchlist timeout "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                duration_string = Methods.clean(message.content[len(command):])

                try:
                    timeout_duration = TimeoutDuration.from_user_string(duration_string)
                except ValueError:
                    handler_response.add(PluginMessageFormats.cannot_parse__timeout_string.format(duration_string))
                    return

                self.handler.state.registered_set(timeout_duration.seconds, "user_watchlist_alert_timeout_seconds", [str(message.author.id)])
                handler_response.add("Watchlist timeout duration set to {0}.".format(timeout_duration.to_user_string()))

    def _private_message__watchlist_add(self, message, handler_response=None):
        command = "!watchlist add "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                target_identifier = Methods.clean(message.content[len(command):])
                target = self.handler.try_get_member(target_identifier, requester_id=message.author.id)

                if target:
                    target_name = self.handler.get_member_name(target, requester_id=message.author.id)
                    watchlist = self.handler.state.registered_get("user_watchlist", [str(message.author.id)])

                    if target.id in watchlist:
                        handler_response.add("{0} is already in your watchlist.".format(target_name))

                    else:
                        self.handler.state.registered_set(watchlist + [target.id], "user_watchlist", [str(message.author.id)])
                        handler_response.add("{0} has been added to your watchlist.".format(target_name))

                else:
                    handler_response.add(PluginMessageFormats.cannot_find_user__identifier.format(target_identifier))

    def _private_message__watchlist_remove(self, message, handler_response=None):
        command = "!watchlist remove "

        if handler_response is not None:
            if message.content[:len(command)].lower() == command:
                target_identifier = Methods.clean(message.content[len(command):])
                target = self.handler.try_get_member(target_identifier, requester_id=message.author.id)
                
                watchlist = self.handler.state.registered_get("user_watchlist", [str(message.author.id)])

                if target:
                    target_name = self.handler.get_member_name(target, requester_id=message.author.id)

                    if target.id in watchlist:
                        self.__remove_watchlist_user(message.author.id, target.id)
                        handler_response.add(MessageFormats.watchlist_user_removed__name.format(target_name))

                    else:
                        handler_response.add("{0} is not in your watchlist.".format(target_name))

                elif target_identifier in [str(target_id) for target_id in watchlist]:
                    target_id = int(target_identifier)

                    self.__remove_watchlist_user(message.author.id, target_id)
                    handler_response.add(MessageFormats.watchlist_user_removed__name.format(target_identifier))

                else:
                    handler_response.add(PluginMessageFormats.cannot_find_user__identifier.format(target_identifier))

    def __remove_watchlist_user(self, author_id, target_id):
        watchlist = self.handler.state.registered_get("user_watchlist", [str(author_id)])

        alert_key = EventKeys.watchlist_alerts.format(author_id, target_id)
        self.handler.try_delete_timeout(alert_key)

        self.handler.state.registered_set(list(filter(lambda user_id: user_id != target_id, watchlist)), "user_watchlist", [str(author_id)])

    def __user_watchlist_status_strings(self, user_id):
        watchlist = self.handler.state.registered_get("user_watchlist", [str(user_id)])
        result = []

        target_statuses = {}

        for target_id in watchlist:
            target = self.handler.try_get_member(target_id)

            if target:
                target_name = self.handler.get_member_name(target, requester_id=user_id)
                target_status_message = SymbolLookup.status[target.status] + " " + target_name
                
                target_statuses[target.status] = target_statuses.get(target.status, []) + [target_status_message]

                alert_key = EventKeys.watchlist_alerts.format(user_id, target.id)
                self.handler.try_delete_timeout(alert_key)  # Reset recipient's timeouts

                if target.status == Status.online:  # Trigger fresh online alert timeouts for the recipient, for any users that this message will show as online
                    new_timeout_duration = TimeoutDuration(self.handler.state.registered_get("user_watchlist_alert_timeout_seconds", [str(user_id)]))
                    self.handler.try_trigger_timeout(alert_key, new_timeout_duration)

            else:
                target_statuses["unknown"] = target_statuses.get("unknown", []) + ["{0} {1} ({2})".format(
                    SymbolLookup.status["unknown"],
                    target_id,
                    PluginMessageFormats.placeholder__cannot_find_user
                )]

        if target_statuses:  # If there is at least one recognised user in the watchlist
            for status in Arguments.status_order:
                result += target_statuses.get(status, [])

            return result