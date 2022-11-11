import os
from discord import Client, Intents

class DiscordClient(Client):
    """
    Base class for a discord bot.

    The general idea is to create component classes
    that are inherited into another class along with 
    DiscordClient, where the primary functionality
    of the bot is activated by `self.trigger_components`.
    """
    TOKEN = os.environ['DiscordToken']
    intents = Intents.default()
    intents.members = True
    intents.presences = True

    def __init__(self):
        super().__init__(intents=self.intents)

    async def on_ready(self):
        await self.trigger_components()
        await self.close()

    async def trigger_components(self):
        pass

    def run(self):
        super().run(self.TOKEN)

def bot_factory(*bot_components):

    class DiscordBot(*bot_components, DiscordClient):
        pass

    return DiscordBot


