import logging

from bot import Bot
from bot.plugins import Watchlist, Dadi

from config import Config

logging.basicConfig(**Config.logging)

try:
    Bot(Config.token, plugins=[Watchlist, Dadi])

except Exception as ex:
    logging.exception(ex)

raise SystemExit
