import shlex

from discord.ext.commands import Converter, Context
from discord.ext.commands._types import BotT

from src.models import ScheduleEventRequest


class CreateEventArgumentDeserializer(Converter):

    async def convert(self, context: Context[BotT], *, arguments: str) -> ScheduleEventRequest:
        parsed_arguments = shlex.split(arguments)  # needs type conversion
        return ScheduleEventRequest(*parsed_arguments)
