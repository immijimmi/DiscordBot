from bot import Bot
from bot.plugins import Watchlist, HelpCommand

from config import Config

Bot(Config.token, plugins=[Watchlist, HelpCommand], log_destination_ids=Config.log_destination_ids)
