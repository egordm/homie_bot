import os
from pathlib import Path
from typing import Iterable

from discord import Guild, TextChannel, Member


def filter_channels(guild: Guild) -> Iterable[TextChannel]:
    for channel in guild.text_channels:
        if is_valid_channel(channel):
            yield channel


def is_valid_channel(channel: TextChannel) -> bool:
    return channel.name == os.getenv('CHANNEL_NAME')


def is_ignored(message: str) -> bool:
    return message.startswith('!') or message.startswith('$')


def is_comment(message: str) -> bool:
    return message.startswith('!')


def format_name(user: Member):
    return user.nick or user.global_name or user.name
