import logging

from bot import Bot
from bot.plugins import Watchlist, HelpCommand

from config import Config

try:
    bot = Bot(
        Config.token,
        plugins=[Watchlist, HelpCommand],
        log_destination_ids=Config.log_destination_ids
        )

except Exception as ex:
    print("An unexpected error has occurred.")
    logging.exception(ex)

    print("\n" + "Press Enter to quit: ")
