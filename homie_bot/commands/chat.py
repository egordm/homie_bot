import re

from discord import Message as DiscordMessage

from langchain.schema import get_buffer_string

from homie_bot.chatting.formatting import format_context, format_messages_buffer
from homie_bot.chatting.llm import llm
from homie_bot.chatting.packing import pack_context
from homie_bot.chatting.retrieval import fetch_context
from homie_bot.db import Session
from homie_bot.models import Message
from homie_bot.utils import is_ignored, is_valid_channel

RETRY_COUNT = 3


async def on_chat_message(
        msg: DiscordMessage,
):
    if msg.author.bot or is_ignored(msg.content):
        return

    if not is_valid_channel(msg.channel):
        return

    with Session() as session:
        session.add(Message(
            message_id=msg.id,
            server=msg.guild.name,
            channel=msg.channel.name,
            username=msg.author.name,
            timestamp=msg.created_at,
            content=msg.content,
        ))
        session.commit()

    await chat(msg)


async def chat(
        ctx_msg: DiscordMessage,
):
    with Session() as session:
        context = await fetch_context(ctx_msg, session)

        context_new = pack_context(context, 7000)

        messages = format_context(context_new)
        messages = format_messages_buffer(messages)

        completion = None
        for _ in range(RETRY_COUNT):
            completion = llm.invoke(messages).content
            completion = clean(completion)
            completion = completion.replace(f'{context.char}: ', '')
            if completion:
                break

        if not completion:
            await ctx_msg.channel.send('!I am sorry, I cannot think of anything to say.')
            return

        await ctx_msg.channel.send(completion)


def clean(msg: str) -> str:
    context = msg.split('\n\n')[0].lstrip('"').rstrip('"')
    context = context.lstrip('"').rstrip('"')

    lines = context.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        if line.startswith('<') or line.startswith('---'):
            break

        if re.match(r'^\w+: ', line) and i > 0:
            break

        new_lines.append(line)

    context = '\n'.join(new_lines)

    return context
