from discord.state import Status

class MessageFormats:
    watchlist_user_online = "{0} is now Online."
    watchlist_welcome_title = "**Your watchlist:**"

class SymbolLookup:
    status = {
        Status.online: ":green_circle:",
        Status.idle: ":orange_circle:",
        Status.dnd: ":red_circle:",
        Status.offline: ":white_circle:",
        Status.invisible: ":black_circle:"
        }
