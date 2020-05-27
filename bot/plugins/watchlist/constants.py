from discord.state import Status

from ...constants import MessageFormats as HandlerMessageFormats

class MessageFormats:
    title__watchlist_private = "**Watchlist:**"

    note__no_watchlist_users = HandlerMessageFormats.format__note.format("Watchlist does not contain any users.")

    watchlist_user_online__name = "{0} is now Online."
    watchlist_user_removed__name = "{0} has been removed from your watchlist."

class EventKeys:
    watchlist_alerts = "user_watchlist_alert|{0}|{1}"
