from discord.state import Status

from ..classes.timeoutDuration import TimeoutDuration
from ..classes.permissions import Permissions
from ..constants import Defaults, MessageFormats as HandlerMessageFormats

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

    visibility = {"public": ":unlock:", "private": ":lock:", "both": ":arrows_clockwise:"}

class MessageFormats:
    note__user_visibility = "*Note: I am only able to see users that I share a server with.*"
    note__timeout_duration = "*Note: Timeout duration must be a number of seconds between 1 and {0}.*".format(TimeoutDuration.max_seconds)
    note__no_nicknames = "*No nicknames set.*"
    note__no_bot_users = "*There are no users with saved settings.*"

    placeholder__cannot_find_user = "unable to find user"

    cannot_find_user = "Unable to find a user based on the provided name." + "\n" + note__user_visibility
    cannot_find_user__identifier = "Unable to find a user based on the name: " + HandlerMessageFormats.format__user_input + "\n" + note__user_visibility
    cannot_parse__timeout_string = "Unable to get a timeout duration from the provided value: " + HandlerMessageFormats.format__user_input + "\n" + note__timeout_duration
    invalid__arguments = "Invalid command arguments: " + HandlerMessageFormats.format__user_input
    nickname_deleted__name_nickname = "Deleted nickname for {0} ({1})."
    cannot_find_nickname__identifier = "No nickname found based on the name: " + HandlerMessageFormats.format__user_input

    _command_template = {
        "": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": ""
            }],
            "children": {}
        }
    }

    commands = {
        "!help": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "provides a list of commands"
            }],
            "children": {}
        },
        "!users": {
            "usage": [{
                "permissions": [Permissions(Permissions.level_admin, [])],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "provides a list of users who have saved settings"
            }],
            "children": {}
        },
        "!settings": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "displays all your settings"
            }, {
                "permissions": [Permissions(Permissions.level_admin, [])],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": ["username#ID, Discord ID or nickname"],
                "description": "displays all the specified user's settings"
            }],
            "children": {}
        },
        "!welcome": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "displays your welcome message settings"
            }, {
                "permissions": [Defaults.permissions],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": ["on/off"],
                "description": "turns welcome messages on or off"
            }],
            "children": {
                "!welcome timeout": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["new timeout duration"],
                        "description": "sets the duration of timeouts on welcome messages to the specified value"
                    }],
                    "children": {}
                }
            }
        },
        "!watchlist": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "displays the statuses of users in your watchlist, and your watchlist settings"
            }, {
                "permissions": [Defaults.permissions],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": ["on/off"],
                "description": "turns watchlist alerts on or off"
            }],
            "children": {
                "!watchlist add": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["username#ID, Discord ID or nickname"],
                        "description": "adds the specified user to your watchlist"
                    }],
                    "children": {}
                },
                "!watchlist remove": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["username#ID, Discord ID or nickname"],
                        "description": "removes the specified user from your watchlist"
                    }],
                    "children": {}
                },
                "!watchlist timeout": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["new timeout duration"],
                        "description": "sets the duration of timeouts on watchlist alerts to the specified value"
                    }],
                    "children": {}
                }
            }
        },
        "!reboot": {
            "usage": [{
                "permissions": [Permissions(Permissions.level_admin, [])],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "updates the code base and reboots the machine the bot is running on"
            }],
            "children": {}
        },
        "!nicknames": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "displays the nicknames you have set for other users"
            }],
            "children": {
                "!nicknames add": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["username#ID, Discord ID or nickname`**{0}**`new nickname".format(Arguments.nickname_separator)],
                        "description": "registers your nickname to the specified user"
                    }],
                    "children": {}
                },
                "!nicknames remove": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["username#ID, Discord ID or nickname"],
                        "description": "deletes the specified nickname"
                    }],
                    "children": {}
                }
            }
        }
    }