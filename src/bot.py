import logging
from pathlib import Path

import discord
import yaml
from discord.ext import commands, tasks

CONFIG_FILE_PATH = Path(__file__).parent / "resources" / "config.yaml"

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

with CONFIG_FILE_PATH.open() as file:
    config = yaml.safe_load(file)
    logger.debug(f"Loaded configuration: {config}")

intents = discord.Intents.default()
bot = commands.Bot(intents=intents, command_prefix='.')
guild = bot.get_guild(config["guildId"])


def activate_handlers():
    # TODO: import all modules specified in config so they can be registered by bot. This acts as a feature toggle as well
    for handler_name in config["active_handlers"]:
        pass
