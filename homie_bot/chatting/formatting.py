from pathlib import Path
from typing import List

import jinja2
from langchain_core.messages import ChatMessage, SystemMessage, HumanMessage, AIMessage, AIMessageChunk, \
    BaseMessageChunk
from langchain.schema import get_buffer_string

from homie_bot.chatting.schema import GenContext, GenMessage

environment = jinja2.Environment()

template_str = Path('bots/template.md').read_text()
template = environment.from_string(template_str)


def format_system_message(**args) -> SystemMessage:
    content = template.render(**args)
    return SystemMessage(content=content)


def format_messages(messages: List[GenMessage], char: str) -> List[AIMessage | HumanMessage]:
    return [
        AIMessage(content=f'{message.author}: {message.content}') if message.author == char
        else HumanMessage(content=f'{message.author}: {message.content}')
        for message in reversed(messages)
    ]


def format_context(context: GenContext) -> List[AIMessage | HumanMessage | SystemMessage]:
    messages = format_messages(context.messages, context.char)

    # if len(messages) > 10:
    #     messages.insert(len(messages) - 3, format_system_message(

    return [
        format_system_message(**context.model_dump()),
        *messages,
        AIMessageChunk(content=f'{context.char}: ')
    ]


def format_messages_buffer(messages: List[AIMessage | HumanMessage | SystemMessage]) -> str:
    text = ''
    for message in messages:
        if isinstance(message, BaseMessageChunk):
            text += message.content
        else:
            text += message.content + '\n'

    return text