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
                "description": "displays the users that are in your watchlist"
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
                        "description": "adds the specified user to your watchlist"
                    }],
                    "children": {}
                }
            }
        }
    }