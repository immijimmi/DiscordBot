import discord

from config import Config
from constants import Data
from discordHandler import DiscordHandler

handler = DiscordHandler(discord.Client())

@client.event
async def on_ready():
    pass 

@client.event
async def on_message(message):
    pass
