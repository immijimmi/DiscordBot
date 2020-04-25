from discord.state import Status

class MessageFormats:
    watchlist_user_online = "{0} is now Online."
    watchlist_title = "**Your watchlist:**"

    status_order = [Status.online, Status.dnd, Status.idle, Status.offline, Status.invisible]

class SymbolLookup:
    status = {
        Status.online: ":green_circle:",
        Status.idle: ":orange_circle:",
        Status.dnd: ":red_circle:",
        Status.offline: ":white_circle:",
        Status.invisible: ":black_circle:"
        }
