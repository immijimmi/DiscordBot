from ...constants import Permissions

class SymbolLookup:
    visibility = {"public": ":unlock:", "private": ":lock:", "both": ":arrows_clockwise:"}

class MessageFormats:
    _command_template = {
        "": {
            "usage": [{
                "permissions_level": Permissions.level_none,
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
                "permissions_level": Permissions.level_none,
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "provides a list of commands"
            }],
            "children": {}
        },
        "!watchlist": {
            "usage": [{
                "permissions_level": Permissions.level_none,
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "displays the statuses of users in your watchlist, and your watchlist settings"
            }],
            "children": {
                "!watchlist add": {
                    "usage": [{
                        "permissions_level": Permissions.level_none,
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["username#ID or Discord ID"],
                        "description": "adds the specified user to your watchlist"
                    }],
                    "children": {}
                },
                "!watchlist remove": {
                    "usage": [{
                        "permissions_level": Permissions.level_none,
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["username#ID or Discord ID"],
                        "description": "removes the specified user from your watchlist"
                    }],
                    "children": {}
                },
                "!watchlist timeout": {
                    "usage": [{
                        "permissions_level": Permissions.level_none,
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
                "permissions_level": Permissions.level_admin,
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "updates the code base and reboots the machine the bot is running on"
            }],
            "children": {}
        }
    }
