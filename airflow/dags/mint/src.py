import os
from src.discord.bot import bot_factory
from discord import ChannelType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium import webdriver
import chromedriver_autoinstaller
from time import sleep
chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

userid = os.environ['DiscordTestUser']
email = os.environ['MintLogin']
password = os.environ['MintPassword']


class VerificationBot:
    """
    Requests a verification code
    via private discord message
    """

    async def send_prompt(self):
        user = await self.fetch_user(userid)
        await user.send("Please respond with your mint verification code.")

        def check(message):
            return (
                message.channel.type == ChannelType.private
                and message.author == user
                )

        message = await self.wait_for(
            'message',
            timeout = 180,
            check=check,
            )

        self.code = message
    
    async def trigger_components(self):
        await self.send_prompt()

def download_transactions(driver, email, password, self, *args, **kwargs) -> None:
    """
    Logs into mint and downloads
    a csv of transaction history
    """
    mint_login(driver, email, password)
    export_data(driver)

def mint_login(
    driver: webdriver.Chrome,
    login: str,
    password: str
    ) -> None:

    driver.get('https://accounts.intuit.com/index.html')
    login_username(driver, login)
    try:
        login_password(driver, password)
        login_auth(driver)
    except:
        login_auth(driver)
    try:
        login_password(driver, password)
    except:
        pass

def login_username(
    driver: webdriver.Chrome,
    login: str
    ) -> None:

    username = WebDriverWait(
        driver, 30
    ).until(
        presence_of_element_located(
            (By.NAME, 'Email')
        )
    )
    username.click()
    username.send_keys(login)
    button = driver.find_element(By.XPATH, "//button[@type='submit']")
    button.click()

def login_password(
    driver: webdriver.Chrome,
    password: str
    ) -> None:

    password_field = WebDriverWait(
        driver, 30
    ).until(
        presence_of_element_located(
            (By.NAME, 'Password')
        )
    )
    password_field.click()
    password_field.send_keys(password)
    button = driver.find_elements(By.XPATH, "//button[@type='submit']")[1]
    button.click()

def login_auth(driver: webdriver.Chrome) -> None:
    auth_code = WebDriverWait(
        driver, 20
    ).until(
        presence_of_element_located(
            (By.NAME, 'Verification code')
        )
    )
    bot = bot_factory(VerificationBot)()  # discord bot
    bot.run()
    verification_code = bot.code.content
    print(verification_code)
    auth_code.send_keys(verification_code)
    button = driver.find_elements(By.XPATH, "//button[@type='submit']")[1]
    button.click()
    sleep(3)
    if driver.find_elements(By.XPATH, "//h4[@data-testid='SelectAccountHeader']"):
        button = driver.find_elements(By.XPATH, "//button[@type='submit']")[1]
        button.click()
    
    
def export_data(driver: webdriver.Chrome) -> None:
    driver.get('https://mint.intuit.com/transaction.event')
    export = WebDriverWait(
        driver, 30
    ).until(
        presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Export')]")
        )
    )
    export.click()
