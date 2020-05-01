import logging

from bot import Bot, Logger
from bot.plugins import Watchlist, Meta

from config import Config

logger = Logger()

try:
    Bot(
        Config.token,
        plugins=[Watchlist, Meta],
        )

except Exception as ex:
    logging.exception(ex)

raise SystemExit
