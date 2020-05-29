from discord.state import Status

from ..classes.timeoutDuration import TimeoutDuration
from ..classes.permissions import Permissions
from ..defaults import Defaults
from ..constants import MessageFormats as HandlerMessageFormats
# from .dadi.constants import PermissionsValues as DadiPermissionsValues  # Circular import - workaround used for the time being

class Arguments:
    nickname_separator = " as: "
    permissions_separator = " "

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
    note__user_visibility = HandlerMessageFormats.format__note.format("Please note that I can only see users that I share a server with.")
    note__preventing_multiple_matches = HandlerMessageFormats.format__note.format("Providing the full username and discriminator - `username#0000` - will prevent multiple users being matched.")
    note__no_nicknames = HandlerMessageFormats.format__note.format("No nicknames set.")
    note__no_bot_users = HandlerMessageFormats.format__note.format("There are no users with saved settings.")
    note__timeout_duration = HandlerMessageFormats.format__note.format("Timeout duration must be a number of seconds between 1 and {0}.".format(TimeoutDuration.max_seconds))

    placeholder__cannot_find_user = "unable to find user"

    multiple_user_matches = "More than one user matches the provided name." + "\n" + note__preventing_multiple_matches
    cannot_find_user = "Unable to find a user based on the provided name." + "\n" + note__user_visibility
    cannot_find_user__identifier = "Unable to find a user based on the name: " + HandlerMessageFormats.format__user_input + "\n" + note__user_visibility
    cannot_parse__timeout_string = "Unable to get a timeout duration from the provided value: " + HandlerMessageFormats.format__user_input + "\n" + note__timeout_duration
    invalid__arguments = "Invalid command arguments: " + HandlerMessageFormats.format__user_input
    nickname_deleted__name_nickname = "Deleted nickname for {0} ({1})."
    cannot_find_nickname__identifier = "No nickname found based on the name: " + HandlerMessageFormats.format__user_input
    permissions_edited__name = "Permissions edited for {0}."

    introductions__username = ["Waddup {0}!", "How's it going {0}?"]

    # Constants for the below commands object
    format__arguments_separator = ">`**{0}**`<"

    admin_permissions = Permissions(Permissions.levels["admin"], [])

    identifier = "Discord username, ID or nickname"

    private = SymbolLookup.visibility["private"]
    public = SymbolLookup.visibility["public"]
    both = SymbolLookup.visibility["both"]

    _command_template = {
        "": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": private,
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
                "visibility": private,
                "arguments": [],
                "description": "provides a list of commands"
            }],
            "children": {}
        },
        "!introduce": {
            "usage": [{
                "permissions": [admin_permissions],
                "visibility": private,
                "arguments": [identifier],
                "description": "sends a greeting message from the bot to the selected user"
            }],
            "children": {}
        },
        "!reboot": {
            "usage": [{
                "permissions": [admin_permissions],
                "visibility": private,
                "arguments": [],
                "description": "updates the code base and reboots the machine the bot is running on"
            }],
            "children": {}
        },
        "!users": {
            "usage": [{
                "permissions": [admin_permissions],
                "visibility": private,
                "arguments": [],
                "description": "provides a list of users who have saved settings"
            }],
            "children": {}
        },
        "!settings": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": private,
                "arguments": [],
                "description": "displays all your settings"
            }, {
                "permissions": [admin_permissions],
                "visibility": private,
                "arguments": [identifier],
                "description": "displays all the specified user's settings"
            }],
            "children": {}
        },
        "!permissions": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": private,
                "arguments": [],
                "description": "displays your current permissions"
            }],
            "children": {
                "!permissions list": {
                    "usage": [{
                        "permissions": [admin_permissions],
                        "visibility": private,
                        "arguments": [],
                        "description": "lists all permissions levels and tags"
                    }],
                    "children": {}
                },
                "!permissions level": {
                    "usage": [{
                        "permissions": [admin_permissions],
                        "visibility": private,
                        "arguments": [("level" + format__arguments_separator + "{1}").format(Arguments.permissions_separator, identifier)],
                        "description": "changes the permissions level of the selected user"
                    }],
                    "children": {}
                },
                "!permissions tag": {
                    "usage": [{
                        "permissions": [admin_permissions],
                        "visibility": private,
                        "arguments": [("tag" + format__arguments_separator + "{1}").format(Arguments.permissions_separator, identifier)],
                        "description": "adds the specified permission tag to the selected user"
                    }],
                    "children": {}
                },
                "!permissions untag": {
                    "usage": [{
                        "permissions": [admin_permissions],
                        "visibility": private,
                        "arguments": [("tag" + format__arguments_separator + "{1}").format(Arguments.permissions_separator, identifier)],
                        "description": "removes the specified permission tag from the selected user"
                    }],
                    "children": {}
                }
            }
        },
        "!welcome": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": private,
                "arguments": [],
                "description": "displays your welcome message settings"
            }, {
                "permissions": [Defaults.permissions],
                "visibility": private,
                "arguments": ["on/off"],
                "description": "turns welcome messages on or off"
            }],
            "children": {
                "!welcome timeout": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": private,
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
                "visibility": private,
                "arguments": [],
                "description": "displays the statuses of users in your watchlist, and your watchlist settings"
            }, {
                "permissions": [Defaults.permissions],
                "visibility": private,
                "arguments": ["on/off"],
                "description": "turns watchlist alerts on or off"
            }],
            "children": {
                "!watchlist add": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": private,
                        "arguments": [identifier],
                        "description": "adds the specified user to your watchlist"
                    }],
                    "children": {}
                },
                "!watchlist remove": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": private,
                        "arguments": [identifier],
                        "description": "removes the specified user from your watchlist"
                    }],
                    "children": {}
                },
                "!watchlist timeout": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": private,
                        "arguments": ["new timeout duration"],
                        "description": "sets the duration of timeouts on watchlist alerts to the specified value"
                    }],
                    "children": {}
                }
            }
        },
        "!nicknames": {
            "usage": [{
                "permissions": [Defaults.permissions],
                "visibility": private,
                "arguments": [],
                "description": "displays the nicknames you have set for other users"
            }],
            "children": {
                "!nicknames add": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": private,
                        "arguments": [("{0}" + format__arguments_separator.format("{1}") + "new nickname").format(identifier, Arguments.nickname_separator)],
                        "description": "registers your nickname to the specified user"
                    }],
                    "children": {}
                },
                "!nicknames remove": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": private,
                        "arguments": [identifier],
                        "description": "deletes the specified nickname"
                    }],
                    "children": {}
                }
            }
        },
        "&kavica": {
            "usage": [{
                "permissions": [
                    # Permissions(Permissions.levels["none"], tags=[DadiPermissionsValues.tag__dadi]),  # Workaround used below
                    Permissions(Permissions.levels["none"], tags=["dadi"]),
                    Permissions(Permissions.levels["none"], tags=[Permissions.tag__hidden]),
                    admin_permissions
                ],
                "visibility": public,
                "arguments": [],
                "description": ""
            }],
            "children": {}
        }
    }