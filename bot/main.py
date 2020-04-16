import discord
from discord.state import Status

from .config import Config
from .discordHandler import Handler
from .extensions import Watchlist

HANDLER = Handler(discord.Client(), extensions=[Watchlist])

@client.event
async def on_ready():
    response = HANDLER.OnReady()

    if response:
        response.Send()

@client.event
async def on_message(message):
    if message.author != HANDLER.client.user:
        response = HANDLER.ProcessMessage(message)

        if response:
            response.Send()

@client.event
async def on_member_update(before, after):
    if before.status != after.status:
        response = HANDLER.StatusChange(before, after)

        if response:
            response.Send()

    if before.status != Status.online and after.status == Status.online:
        if after != HANDLER.client.user:
            response = HANDLER.UserOnline(before, after)

            if response:
                response.Send()
