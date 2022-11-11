import os
from src.discord.bot import bot_factory
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults
from airflow.operators.python_operator import PythonOperator


class DiscordOperator(PythonOperator):

    TOKEN = os.environ['DiscordBot']

    @apply_defaults
    def __init__(
        self,
        bot_components,
        *args,
        **kwargs):

        super().__init__(*args, **kwargs)
        self.bot_components = bot_components

    def execute(self, context):
        bot = bot_factory(self.bot_components)
        self.op_args = [bot] + self.op_args
        callable_return = super().execute(context)
        return callable_return


class DiscordPlugin(AirflowPlugin):
    name = "discord_plugin"
    operators = [DiscordOperator]
