import random
from typing import Callable, List, Any

from langchain_core.messages import get_buffer_string
from pydantic import BaseModel

from homie_bot.chatting.formatting import template, format_system_message, format_messages, format_context
from homie_bot.chatting.llm import token_count_fn
from homie_bot.chatting.schema import GenContext, GenMessage

TokenCountFn = Callable[[str], int]


class PackingConfig(BaseModel):
    token_count_fn: TokenCountFn
    token_limit: int
    min_items: int = 1
    max_items: int = 1000


def pack_prompt(
        format_fn: Callable[[List[Any]], str],
        items: List[Any],
        config: PackingConfig,
) -> List[Any]:
    packed_items = [
        items[i] for i in range(min(len(items), config.max_items))
    ]

    while packed_items:
        if len(packed_items) <= config.min_items:
            break

        if config.token_count_fn(format_fn(packed_items)) < config.token_limit:
            break

        packed_items.pop()

    return packed_items


MIN_EXAMPLES = 6
MIN_MESSAGES = 20
MAX_LORE_ENTRIES = 10
MIN_PERSON_ENTRIES = 4


def pack_context(context: GenContext, token_limit: int):
    new_context = GenContext(
        char=context.char,
        char_info=context.char_info,
        important=context.important,
        user=context.user,
        datetime=context.datetime,
        examples=[],
        messages=[],
        persons=[],
        lores=[],
    )

    num_examples_to_add = min(max(MIN_EXAMPLES, MIN_MESSAGES - len(context.messages)), len(context.examples))
    new_context.examples = random.sample(context.examples, num_examples_to_add)

    num_lores_to_add = min(len(context.lores), MAX_LORE_ENTRIES)
    new_context.lores = random.sample(context.lores, num_lores_to_add)

    num_persons_to_add = min(len(context.persons), MIN_PERSON_ENTRIES)
    new_context.persons = context.persons[:num_persons_to_add]

    def format_context_messages(messages: List[GenMessage]):
        data = context.model_dump()
        data['messages'] = messages

        chat = format_context(GenContext(**data))

        return get_buffer_string(chat)

    messages = pack_prompt(
        format_fn=format_context_messages,
        items=context.messages,
        config=PackingConfig(
            token_count_fn=token_count_fn,
            token_limit=token_limit,
        ),
    )
    new_context.messages = messages

    def format_context_persons(persons: List[GenMessage]):
        data = context.model_dump()
        data['persons'] = [
            *context.persons,
            *persons,
        ]

        chat = format_context(GenContext(**data))

        return get_buffer_string(chat)

    persons = pack_prompt(
        format_fn=format_context_persons,
        items=context.persons[num_persons_to_add:],
        config=PackingConfig(
            token_count_fn=token_count_fn,
            token_limit=token_limit,
        ),
    )
    new_context.persons = [
        *new_context.persons,
        *persons,
    ]

    return new_context
