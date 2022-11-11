from discord import Client, Intents

class DiscordClient(Client):
    """
    Base class for a discord bot.

    The general idea is to create component classes
    that are inherited into another class along with 
    DiscordClient, where the primary functionality
    of the bot is activated by `self.start()`.
    """

    intents = Intents.default()
    intents.members = True
    intents.presences = True

    async def on_ready(self):
        self.start()
        self.close()

def bot_factory(*bot_components):

    class DiscordBot(DiscordClient, *bot_components):
        pass

    return DiscordBot

def start(self):
    pass
