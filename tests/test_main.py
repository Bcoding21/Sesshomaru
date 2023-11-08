import pytest
from pytest_mock import MockerFixture

from src.main import on_ready


def test_on_ready_creates_event():
    on_ready()


@pytest.fixture()
def commands(mocker: MockerFixture):
    return mocker.patch("src.main.command")


@pytest.fixture()
def bot(commands):
    return commands.Bot.return_value


@pytest.fixture()
def guild(bot):
    return bot.get_guild.
