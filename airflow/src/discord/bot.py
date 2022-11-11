from discord import Client, Intents

class DiscordClient(Client):

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
