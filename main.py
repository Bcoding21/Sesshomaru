from typing import Tuple

import discord
from discord.ext import commands, tasks
from discord.utils import get
import pytz
import json
from datetime import datetime, timedelta
import logging

AMERICA_NEW_YORK_TIMEZONE = pytz.timezone("America/New_York")
CONFIG_FILE_PATH = "botConfig.json"

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

with open(CONFIG_FILE_PATH, "r") as file:
    config = json.load(file)
    logger.debug(f"Loaded configuration: {config}")

intents = discord.Intents.default()
bot = commands.Bot(intents=intents, command_prefix='.')
guild = bot.get_guild(config["guildId"])


@bot.event
async def on_ready():
    logger.info(f"Logged in. Username: {bot.user}")
    event_information = config["eventList"][0]
    event_name = event_information["name"]

    if await does_event_exist(event_name):
        logger.info(f"Event {event_name} already exist")
        return

    event = create_event(event_information)
    logger.info(f"Creating event: {event}")
    await guild.create_scheduled_event(**event)
    logger.info(f"Successfully created event: {event_name}")


async def does_event_exist(event_name: str) -> bool:
    events = await guild.fetch_scheduled_events()
    return any(event.name == event_name for event in events)


def create_event(event_information: dict) -> dict:
    event_start_hour = event_information["startTime"]["hour"]
    event_start_minute = event_information["startTime"]["minute"]
    start_date, end_date = _determine_start_and_end_date(event_start_hour, event_start_minute)

    return {
        "name": event_information["name"],
        "description": event_information["description"],
        "start_time": start_date,
        "end_time": end_date,
        "entity_type": discord.EntityType.external,
        "privacy_level": discord.PrivacyLevel.guild_only,
        "location": "",
    }


def _determine_start_and_end_date(start_hour: int, start_minute: int) -> Tuple[datetime, datetime]:
    current_date = datetime.now(AMERICA_NEW_YORK_TIMEZONE)
    days_until_monday = (7 - current_date.weekday()) % 7
    next_mondays_date = timedelta(days=days_until_monday) + current_date
    start_date = next_mondays_date.replace(hour=start_hour, minute=start_minute)
    end_date = start_date + timedelta(hours=1)
    return start_date, end_date


# Start the bot.
bot.run(config["token"])
