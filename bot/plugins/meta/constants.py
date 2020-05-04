from ...constants import Defaults
from ...classes.permissions import Permissions
from ..constants import Arguments

class SymbolLookup:
    visibility = {"public": ":unlock:", "private": ":lock:", "both": ":arrows_clockwise:"}

class MessageFormats:
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
                        "arguments": ["username#ID or Discord ID"],
                        "description": "adds the specified user to your watchlist"
                    }],
                    "children": {}
                },
                "!watchlist remove": {
                    "usage": [{
                        "permissions": [Defaults.permissions],
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["username#ID or Discord ID"],
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
                        "arguments": ["username#ID or Discord ID`{0}`nickname".format(Arguments.nickname_separator)],
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
