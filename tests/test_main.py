from types import SimpleNamespace
from unittest.mock import Mock, AsyncMock

import pytest
from discord import Forbidden
from discord.ext.commands import Context
from pytest_mock import MockerFixture

from src.handlers.events import create_event
from src.models import ScheduleEventRequest


@pytest.mark.asyncio
@pytest.mark.parametrize("scheduled_events", [
    [SimpleNamespace(name="test2"), SimpleNamespace(name="test3")],
    []
])
async def test_create_event__event_doesnt_exist__creates_event(context: Mock, scheduled_events: list):
    context.guild.fetch_scheduled_events.return_value = scheduled_events
    event = ScheduleEventRequest(name="test")

    await create_event(context, event)

    context.guild.create_scheduled_event.assert_called()
    context.send.assert_called_with("Event test created by Brandon")


@pytest.mark.asyncio
async def test_create_event__event_exist__does_not_create_event(context: Mock):
    context.guild.fetch_scheduled_events.return_value = [SimpleNamespace(name="test")]
    event = ScheduleEventRequest(name="test")

    await create_event(context, event)

    context.guild.create_scheduled_event.assert_not_called()
    context.send.assert_called_with("Could not create event test")


@pytest.mark.asyncio
@pytest.mark.parametrize("exception", [Exception, Forbidden, TypeError])
async def test_create_event__error_creating_event__does_not_create_event(context: Mock, exception: Exception):
    context.guild.fetch_scheduled_events.side_effect = exception
    event = ScheduleEventRequest(name="test")

    await create_event(context, event)

    context.guild.create_scheduled_event.assert_not_called()
    context.send.assert_called_with("Could not create event test")


@pytest.fixture()
def context(mocker: MockerFixture) -> Context:
    context = mocker.Mock(spec=Context)
    context.author.id = "Brandon"
    context.guild.fetch_scheduled_events = AsyncMock(return_value=[])
    context.guild.create_scheduled_event = AsyncMock(return_value=None)
    context.send = AsyncMock(return_value=None)
    return context
