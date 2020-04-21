import discord
from discord.state import Status

from .config import Config
from .discordHandler import Handler
from .plugins.watchlist.watchlist import Watchlist

HANDLER = Handler(discord.Client(), plugins=[Watchlist])

@HANDLER.client.event
async def on_ready():
    responses = HANDLER.on_ready()

    await Handler.send_responses(responses)

@HANDLER.client.event
async def on_message(message):
    if message.author != HANDLER.client.user:
        responses = HANDLER.process_message(message)

        await Handler.send_responses(responses)

@HANDLER.client.event
async def on_member_update(before, after):
    if before.status != Status.online and after.status == Status.online:
        if after != HANDLER.client.user:
            responses = HANDLER.user_online(before, after)

            await Handler.send_responses(responses)

HANDLER.client.run(Config.token)
