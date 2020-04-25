class SymbolLookup:
    visibility = {"public": ":unlock:", "private": ":lock:", "both": ":arrows_clockwise:"}

class MessageFormats:
    _command_template = {
        "": {
            "usage": [{
                "visibility": SymbolLookup.visibility,
                "arguments": [],
                "description": ""
            }],
            "children": {}
        }
    }

    commands = {
        "!help": {
            "usage": [{
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "provides a list of commands"
            }],
            "children": {}
        },
        "!watchlist": {
            "usage": [{
                "visibility": SymbolLookup.visibility["private"],
                "arguments": [],
                "description": "displays the users that are in your watchlist"
            }],
            "children": {
                "!watchlist add": {
                    "usage": [{
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["username#ID or Discord ID"],
                        "description": "adds the specified user to your watchlist"
                    }],
                    "children": {}
                },
                "!watchlist remove": {
                    "usage": [{
                        "visibility": SymbolLookup.visibility["private"],
                        "arguments": ["username#ID or Discord ID"],
                        "description": "adds the specified user to your watchlist"
                    }],
                    "children": {}
                }
            }
        }
    }