from discord.state import Status

class MessageFormats:
    title__watchlist_private = "**Your watchlist:**"

    watchlist_user_online__name = "{0} is now Online."
    watchlist_user_removed__name = "{0} has been removed from your watchlist."

class EventKeys:
    watchlist_alerts = "user_watchlist_alert|{0}|{1}"
