import os
from .discord.bot import bot_factory
from discord import ChannelType

userid = os.environ['DiscordTestUser']

class VerificationBot:

    async def send_prompt(self):
        user = await self.fetch_user(userid)
        await user.send("Please response with your mint verification code.")

        def check(message):
            return (
                message.channel.type == ChannelType.private
                and message.author == user
                )

        message = await self.wait_for(
            'message',
            timeout = 30,
            check=check,
            )

        return message.content
    
    async def trigger_components(self):
        await self.send_prompt()

# INCOMPLETE
    # requires development of discord hook
def mint_login(driver, email, password):
    driver.get('https://accounts.intuit.com'
               '/index.html'
               '?offering_id=Intuit.ifs.mint&namespace_id=50000026'
               '&redirect_url=https%3A%2F%2Fmint.intuit.com'
               '%2Foverview.event%3Futm_medium%3Ddirect%26cta%3Dnav_login_dropdown')
    
    username = driver.find_element_by_name('Email')
    username.click()
    username.send_keys(email)
    button = driver.find_element_by_xpath("//button[@type='submit']")
    button.click()
    password = driver.find_element_by_name('Password')
    password.send_keys(password)
    button = driver.find_element_by_xpath("//button[@type='submit']")
    button.click()
    
    text_auth = driver.find_element_by_xpath('//button[@data-testid="challengePickerOption_SMS_OTP"]')
    text_auth.click()
    
    auth_code = driver.find_element_by_name('Verification code')
    bot = bot_factory(VerificationBot)
    verification_code = bot().run()
    auth_code.send_keys(verification_code)
    
    
def export_data(driver):
    driver.get('https://mint.intuit.com/transaction.event')
    export = driver.find_element_by_xpath('//button[contains(., "Export")]')
    export.click()