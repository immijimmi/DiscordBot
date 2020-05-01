import logging

from bot import Bot
from bot.plugins import Watchlist, Meta

from config import Config

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s|%(levelname)s:%(message)s"
    )  # Temporary logging solution

try:
    Bot(Config.token, plugins=[Watchlist, Meta])

except Exception as ex:
    logging.exception(ex)

raise SystemExit
