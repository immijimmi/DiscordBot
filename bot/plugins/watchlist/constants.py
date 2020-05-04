from discord.state import Status

class MessageFormats:
    watchlist_user_online = "{0} is now Online."
    watchlist_user_removed = "{0} has been removed from your watchlist."
    watchlist_title_private = "**Your watchlist:**"

    status_order = [Status.online, Status.dnd, Status.idle, Status.offline, Status.invisible, "unknown"]

class EventKeys:
    watchlist_alerts = "user_watchlist_alert|{0}|{1}"
