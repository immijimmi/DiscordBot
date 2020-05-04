from discord.state import Status

from ..classes.timeoutDuration import TimeoutDuration
from ..constants import MessageFormats as HandlerMessageFormats

class MessageFormats:
    note__user_visibility = "*Please note that I am only able to see users I share a server with.*"
    note__timeout_duration = "*Timeout duration must be a number of seconds between 1 and {0}.*".format(TimeoutDuration.max_seconds)

    placeholder__cannot_find_user = "unable to find user"

    cannot_find_user = "Unable to find a user based on the provided name." + "\n" + note__user_visibility
    cannot_find_user__identifier = "Unable to find a user based on the name: " + HandlerMessageFormats.format__user_input + "\n" + note__user_visibility
    cannot_parse__timeout_string = "Unable to get a timeout duration from the provided value: " + HandlerMessageFormats.format__user_input + "\n" + note__timeout_duration
    invalid__arguments = "Invalid command arguments: " + HandlerMessageFormats.format__user_input
    nickname_deleted__name_nickname = "Deleted nickname for {0} ({1})."
    cannot_find_nickname__identifier = "No nickname found based on the name: " + HandlerMessageFormats.format__user_input

class Arguments:
    nickname_separator = " as: "

    toggle_change_strings = ["toggle"]
    toggle_on_strings = ["on", "enable", "enabled"]
    toggle_off_strings = ["off", "disable", "disabled"]

    status_order = [Status.online, Status.dnd, Status.idle, Status.offline, Status.invisible, "unknown"]

class SymbolLookup:
    status = {
        Status.online: ":green_circle:",
        Status.idle: ":orange_circle:",
        Status.dnd: ":red_circle:",
        Status.offline: ":white_circle:",
        Status.invisible: ":black_circle:",
        "unknown": ":grey_question:"
        }
