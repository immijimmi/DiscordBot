from discord.state import Status

from objectExtensions import Extension

from ..discordHandler import Handler
from ..responseBuilder import ResponseBuilder
from ..constants import KeyQueryFactories
from .constants import ResponseFormats

class Watchlist(Extension):
    @staticmethod
    def extend(target_instance):
        Watchlist._register_paths(target_instance)

        Extension.wrap(target_instance, "user_online", after=Watchlist._online_alert)

    @staticmethod
    def can_extend(target_instance):
        return type(target_instance) is Handler

    @staticmethod
    def _register_paths(target_instance):
        target_instance.state.register("user_watchlist", ["user_settings", KeyQueryFactories.user_id, "watchlist"], [{}, {}, []])

    @staticmethod
    def _online_alert(metadata):
        handler = metadata["self"]
        online_user = metadata["args"][1]

        all_saved_users = [user_id for user_id in handler.state.registered_get("all_users_settings")]

        for user_id in all_saved_users:
            user_watchlist = handler.state.registered_get(["user_watchlist"], [user_id])

            if online_user.id in user_watchlist:
                watcher = handler.get_member(user_id)

                if watcher.status == Status.online:
                    response = ResponseBuilder([watcher])
                    response.add(ResponseFormats.watchlist_user_online.format(handler.get_member_name(online_user, watcher)))

                    handler.responses_working.append(response)
