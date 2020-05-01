import discord
from discord import TextChannel, VoiceChannel, DMChannel, GroupChannel
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
        if message.author == self.user:
            return
        if message.channel.id in self.logger.destination_ids:
            return

        is_private = isinstance(message.channel, DMChannel)
        if is_private:
            await self.handler.process_private_message(message)
        else:
            await self.handler.process_public_message(message)

    async def on_member_update(self, before, after):
        if after == self.user:
            return
        
        if before.status != Status.online and after.status == Status.online:
            await self.handler.user_online(before, after)

        elif before.status == Status.online and after.status != Status.online:
            await self.handler.user_away(before, after)
