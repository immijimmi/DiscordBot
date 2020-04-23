import discord
from discord.state import Status

from .discordHandler import Handler

class Bot(discord.Client):
    def __init__(self, token, plugins=[]):
        super().__init__()
        
        self.handler = Handler(self, plugins=plugins)

        self.run(token)
    
    async def on_ready(self):
        await self.handler.on_ready()

    async def on_message(self, message):
        if message.author != self.user:
            await self.handler.process_message(message)

    async def on_member_update(self, before, after):
        if before.status != Status.online and after.status == Status.online:
            if after != self.handler.client.user:
                await self.handler.user_online(before, after)
