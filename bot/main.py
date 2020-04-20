import discord
from discord.state import Status

from .config import Config
from .discordHandler import Handler
from .extensions.watchlist.watchlist import Watchlist

HANDLER = Handler(discord.Client(), extensions=[Watchlist])

@HANDLER.client.event
async def on_ready():
    HANDLER.on_ready()

    await HANDLER.send_responses()

@HANDLER.client.event
async def on_message(message):
    if message.author != HANDLER.client.user:
        HANDLER.process_message(message)

        await HANDLER.send_responses()

@HANDLER.client.event
async def on_member_update(before, after):
    if before.status != Status.online and after.status == Status.online:
        if after != HANDLER.client.user:
            HANDLER.user_online(before, after)

            await HANDLER.send_responses()

HANDLER.client.run(Config.token)
