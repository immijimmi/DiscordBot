import logging

from bot import Bot
from bot.plugins import Watchlist, Meta

from config import Config

try:
    Bot(
        Config.token,
        plugins=[Watchlist, Meta],
        log_destination_ids=Config.log_destination_ids
        )

except Exception as ex:
    print("An unexpected error has occurred.")
    logging.exception(ex)

input("\n" + "Press Enter to quit: ")
raise SystemExit
