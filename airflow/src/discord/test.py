import os
from bot import bot_factory

userid = os.environ['DiscordTestUser']

class DiscordTest:
    
    async def sendDm(self):
        print('Triggering')
        user = await self.fetch_user(userid)
        print(user)
        await user.send("Hello world")
        return ''

    async def trigger_components(self):
        await self.sendDm()

if __name__ == "__main__":
    bot = bot_factory(DiscordTest)
    bot().run()
