import logging

from bot import Bot
from bot.plugins import Watchlist, Meta

from config import Config

logging.basicConfig(**Config.logging)

try:
    Bot(Config.token, plugins=[Watchlist, Meta])

except Exception as ex:
    logging.exception(ex)

raise SystemExit
