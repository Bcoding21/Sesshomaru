"""
Import bot from bot.py
use it to respond

"""
from discord.ext.commands import Context

from src.bot import bot


@bot.command(name="Chat")
async def respond_to_user(context: Context, text: str):
    # TODO: do implementation
    response = "None"
    await context.send(response)
