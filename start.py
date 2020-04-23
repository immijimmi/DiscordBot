from bot import Bot
from bot.plugins.watchlist import Watchlist

from config import Config

Bot(Config.token, plugins=[Watchlist])
