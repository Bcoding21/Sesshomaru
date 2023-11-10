from dataclasses import asdict
from typing import Tuple

from discord.ext.commands import Context
import pytz
from datetime import datetime, timedelta
import logging

from src.deserializers import CreateEventArgumentDeserializer
from src.bot import bot

AMERICA_NEW_YORK_TIMEZONE = pytz.timezone("America/New_York")

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


@bot.command(name="Create Event")
async def create_event(context: Context, request: CreateEventArgumentDeserializer):
    logger.info(f"Received request from {context.author.id} to create event {request}")

    try:
        logger.info(f"Determining if event already exist")
        scheduled_events = await context.guild.fetch_scheduled_events()
        does_event_exist = any(
            scheduled_event.name == request.name for scheduled_event in scheduled_events)

        if does_event_exist:
            raise ValueError("Event already exist")

        logger.info("Creating event")
        await context.guild.create_scheduled_event(**asdict(request))
        logger.info(f"Successfully created event: {request.name}")
        await context.send(f"Event {request.name} created by {context.author.id}")

    except Exception as e:
        logger.exception("Could not create event", exc_info=e)
        await context.send(f"Could not create event {request.name}")


@bot.command(name="Delete Event")
async def delete_event(context: Context,
                       delete_event_request: CreateEventArgumentDeserializer):  # TODO: create arguement deserializer
    # TODO: implement

    pass


@bot.command(name="Update Event")
async def update_event(context: Context,
                       update_event_request: CreateEventArgumentDeserializer):  # TODO: create arguement deserializer
    # TODO: implement
    pass


def _determine_start_and_end_date(start_hour: int, start_minute: int, duration: int) -> Tuple[datetime, datetime]:
    current_date = datetime.now(AMERICA_NEW_YORK_TIMEZONE)
    days_until_monday = (7 - current_date.weekday()) % 7
    next_mondays_date = current_date + timedelta(days=days_until_monday)
    start_date = next_mondays_date.replace(hour=start_hour, minute=start_minute)
    end_date = start_date + timedelta(hours=duration)
    return start_date, end_date
