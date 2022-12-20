import time
import logging

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from airflow.models import BaseOperator
from airflow.hooks.base_hook import BaseHook
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults


class SeleniumChromeHook(BaseHook):
    '''
    Creates a Selenium Docker container on the host and controls the
    browser by sending commands to the remote server.
    '''
    def __init__(self, download_dir=''):
        logging.info('initialised hook')
        self.chromedriver = "http://chrome:4444"
        self.download_dir = download_dir

    def test_selenium_server_available(self):
        session = requests.Session()
        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        session.get(self.chromedriver)

    def create_driver(self):
        '''
        creates and configure the remote Selenium webdriver.
        '''
        logging.info('creating driver')
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("window-size=1400,2100") 
        options.add_argument('--disable-gpu')
        download_dir = {'download.default_directory' : '/home/seluser/files/' + self.download_dir}
        options.add_experimental_option('prefs', download_dir)
        while True:
            try:
                driver = webdriver.Remote(
                    command_executor=self.chromedriver,
                    desired_capabilities=DesiredCapabilities.CHROME,
                    options=options)
                print('remote ready')
                break
            except:
                print('remote not ready, sleeping for ten seconds.')
                time.sleep(10)

        self.driver = driver

    def run_script(self, script, args, kwargs):
        '''
        This is a wrapper around the python script which sends commands to
        the docker container. The first variable of the script must be the web driver.
        '''
        output = script(self.driver, *args, **kwargs)
        self.driver.quit()
        return output

    def get_cookies(self) -> dict:
        cookies = {}
        selenium_cookies = self.driver.get_cookies()
        for cookie in selenium_cookies:
            cookies[cookie['name']] = cookie['value']
        return cookies


class SeleniumChromeOperator(BaseOperator):
    '''
    Selenium Chrome Operator
    '''
    template_fields = ['script_args']

    @apply_defaults
    def __init__(self,
                 script,
                 script_args=[],
                 script_kwargs={},
                 provide_context=True,
                 download_dir='',
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.script = script
        self.script_args = script_args
        self.script_kwargs = script_kwargs
        self.provide_context = provide_context
        self.download_dir = download_dir

    def execute(self, context):
        hook = SeleniumChromeHook(download_dir=self.download_dir)
        hook.create_driver()
        if self.provide_context:
            self.script_kwargs.update(context)

        return hook.run_script(
            self.script, 
            self.script_args, 
            self.script_kwargs
            )


class SeleniumPlugin(AirflowPlugin):
    name = 'selenium_plugin'
    operators = [SeleniumChromeOperator]
    hooks = [SeleniumChromeHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
