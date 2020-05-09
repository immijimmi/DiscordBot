import logging

from bot import Bot
from bot.plugins import Watchlist

from config import Config

logging.basicConfig(**Config.logging)

try:
    Bot(Config.token, plugins=[Watchlist])

except Exception as ex:
    logging.exception(ex)

raise SystemExit
