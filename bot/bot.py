import discord
from discord.state import Status

from .discordHandler import Handler
from .classes.discordLogger import Logger

class Bot(discord.Client):
    def __init__(self, token, plugins=[], log_destination_ids=[]):
        super().__init__()
        
        self.logger = Logger(self, destination_ids=log_destination_ids)
        self.handler = Handler(self, plugins=plugins)

        self.run(token)
    
    async def on_ready(self):
        await self.handler.on_ready()

    async def on_message(self, message):
        if message.author == self.user:
            return

        message_destination_ids = [recipient.id for recipient in message.channel.recipients] + [message.channel.id]
        if any([log_destination_id in message_destination_ids for log_destination_id in self.logger.destination_ids]):
            return

        if message.channel.is_private:
            await self.handler.process_private_message(message)

        else:
            await self.handler.process_public_message(message)

    async def on_member_update(self, before, after):
        if before.status != Status.online and after.status == Status.online:
            if after != self.handler.client.user:
                await self.handler.user_online(before, after)
