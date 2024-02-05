import os
import re
from pathlib import Path
from typing import List
import datetime as dt

from discord import Message as DiscordMessage
from sqlalchemy.orm import Session as SQLSession

from homie_bot.chatting.schema import GenContext, Person, GenMessage, CharacterData, GenLore
from homie_bot.logging import logger
from homie_bot.models import Message, UserInfo, Lore
from homie_bot.utils import format_name, is_ignored

CONTEXT_MESSAGE_COUNT = 100
LORE_SEARCH_WINDOW = 30

NAME_CACHE = {}


async def fetch_context(msg: DiscordMessage, session: SQLSession) -> GenContext:
    global NAME_CACHE
    char_data = load_char(os.getenv('BOT_NAME'), os.getenv("BOT_PATH"))

    if msg.guild.name not in NAME_CACHE:
        name_lookup = {}

        for user in msg.guild.members:
            name_lookup[user.name] = format_name(user)

        name_lookup[msg.author.name] = format_name(msg.author)

        NAME_CACHE[msg.guild.name] = name_lookup
    else:
        name_lookup = NAME_CACHE[msg.guild.name]

    recent_messages: List[Message] = await fetch_last_messages(msg)
    logger.info(f'Retrieved {len(recent_messages)} recent messages for {msg.channel.name}...')

    usernames_set = set()
    usernames = []
    for message in recent_messages:
        if message.username not in usernames_set:
            usernames_set.add(message.username)
            usernames.append(message.username)

    backstories = (
        session
        .query(UserInfo)
        .filter_by(server=msg.guild.name)
        .all()
    )
    logger.info(f'Retrieved {len(backstories)} backstories for {msg.channel.name}...')

    backstories = {
        backstory.username: backstory
        for backstory in backstories
    }
    other_usernames = set(backstories.keys()) - set(usernames)
    persons = [
        Person(
            name=name_lookup.get(username, username),
            backstory=backstories[username].backstory,
        )
        for username in [*usernames, *other_usernames]
        if username in backstories
    ]

    lores = (
        session
        .query(Lore)
        .filter_by(server=msg.guild.name, channel=msg.channel.name)
        .all()
    )
    logger.info(f'Retrieved {len(lores)} lores for {msg.channel.name}...')

    lores = [
        Lore(
            names=lore.names,
            content=lore.content,
        )
        for lore in lores
    ]

    messages = [
        GenMessage(
            author=name_lookup.get(msg.username, msg.username),
            content=msg.content,
        )
        for msg in recent_messages
    ]

    lores = filter_relevant_lores(lores, messages[:LORE_SEARCH_WINDOW])
    lores = [
        GenLore(
            names=lore.names,
            content=lore.content,
        )
        for lore in lores
    ]

    return GenContext(
        char=char_data.char,
        char_info=char_data.char_info,
        examples=char_data.examples,
        important=char_data.important,
        datetime=dt.datetime.now().strftime("%d, %b %Y %H:%M:%S"),
        user=name_lookup.get(msg.author.name, msg.author.name),
        persons=persons,
        lores=lores,
        messages=messages,
    )


def message_has_lore(msg: GenMessage, lore: Lore) -> bool:
    return lore.names in msg.content


def filter_relevant_lores(lores: List[Lore], messages: List[GenMessage]) -> List[Lore]:
    regexes = []
    for lore in lores:
        names = [re.escape(name.strip().lower()) for name in lore.names.split(',')]
        regex = re.compile('|'.join(names))
        regexes.append(dict(
            regex=regex,
            lore=lore,
            added=False,
        ))

    relevant_lores = []
    for message in messages:
        for item in regexes:
            if item['added']:
                continue

            regex = item['regex']
            lore = item['lore']
            if regex.search(message.content.lower()):
                relevant_lores.append(lore)
                item['added'] = True

    return relevant_lores


def load_char(name: str, prefix: str) -> CharacterData:

    char_info = Path(f'bots/{prefix}/info.md').read_text().strip()
    examples_text = Path(f'bots/{prefix}/examples.md').read_text().strip()
    examples = [
        example.strip()
        for example in examples_text.split('---')
    ]
    important = Path(f'bots/{prefix}/important.md').read_text().strip()

    return CharacterData(
        char=name,
        char_info=char_info,
        examples=examples,
        important=important,
    )


async def fetch_last_messages(msg: DiscordMessage) -> List[Message]:
    messages = [
        message async
        for message in msg.channel.history(
            limit=100,
        )
    ]

    result = []
    for message in messages:
        if message.content == '$reset':
            break

        if is_ignored(message.content):
            continue

        result.append(Message(
            message_id=message.id,
            server=msg.guild.name,
            channel=msg.channel.name,
            username=message.author.name,
            timestamp=message.created_at,
            content=message.content,
        ))

    return result
