import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import discord
import yaml
from discord.ext import commands, tasks
from discord.ext.commands import Context, Converter
from discord.ext.commands._types import BotT
from discord.ext.commands.converter import T_co
from discord.utils import get
import pytz
import json
from datetime import datetime, timedelta
import logging

AMERICA_NEW_YORK_TIMEZONE = pytz.timezone("America/New_York")
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


@dataclass
class Event:
    name: str
    description: str
    day: str
    start_time: str
    start_minute: str
    duration: str


class CreateEventArgumentConverter(Converter):

    async def convert(self, context: Context[BotT], *, arguments: str) -> Event:
        parsed_arguments = shlex.split(arguments)  # needs type conversion
        return Event(*parsed_arguments)


@bot.command(name="Create Event")
async def create_event(context: Context, event: CreateEventArgumentConverter):
    logger.info(f"Received request from {context.author.id} to create event {event}")

    scheduled_events = await context.guild.fetch_scheduled_events()
    does_event_exist = any(scheduled_event.name == event.name for scheduled_event in scheduled_events)

    if does_event_exist:
        logger.info(f"Event {event.name} already exist")
        await context.send(f"Hi {context.author.id}. I could not create this event. It is already scheduled.")
        return

    logger.info("Creating event")
    await guild.create_scheduled_event(**event)
    logger.info(f"Successfully created event: {event.name}")




@bot.event
async def on_ready():
    logger.info(f"Logged in. Username: {bot.user}")

    for event_information in config["events"]:
        event_name = event_information["name"]

        if await does_event_exist(event_name):
            logger.info(f"Event {event_name} already exist")
            return

        event = create_event(event_information)
        logger.info(f"Creating event: {event}")
        await guild.create_scheduled_event(**event)
        logger.info(f"Successfully created event: {event_name}")


async def does_event_exist(event_name: str) -> bool:
    return any(event.name == event_name for event in await guild.fetch_scheduled_events())


def create_event(event_information: dict) -> dict:
    event_start_hour = event_information["start_hour"]
    event_start_minute = event_information["start_minute"]
    event_duration = event_information["duration"]
    start_date, end_date = _determine_start_and_end_date(event_start_hour, event_start_minute, event_duration)

    return {
        "name": event_information["name"],
        "description": event_information["description"],
        "start_time": start_date,
        "end_time": end_date,
        "entity_type": discord.EntityType.external,
        "privacy_level": discord.PrivacyLevel.guild_only,
        "location": "",
    }


def _determine_start_and_end_date(start_hour: int, start_minute: int, duration: int) -> Tuple[datetime, datetime]:
    current_date = datetime.now(AMERICA_NEW_YORK_TIMEZONE)
    days_until_monday = (7 - current_date.weekday()) % 7
    next_mondays_date = current_date + timedelta(days=days_until_monday)
    start_date = next_mondays_date.replace(hour=start_hour, minute=start_minute)
    end_date = start_date + timedelta(hours=duration)
    return start_date, end_date


if __name__ == '__main__':
    args = "Brandon \"Clinton Cole\""
    print(shlex.split(args))
    # bot.run(config["token"])
