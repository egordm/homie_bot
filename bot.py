import os
from dotenv import load_dotenv

load_dotenv()

import discord
from discord import Message
from discord.ext import commands

from homie_bot.commands import init_commands
from homie_bot.commands.chat import on_chat_message
# noinspection PyUnresolvedReferences
from homie_bot.db import engine, Session
from homie_bot.logging import logger
from homie_bot.utils import is_valid_channel

intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True


class ComradeBot(commands.Bot):
    async def on_message(self, message: Message) -> None:
        if message.content.startswith(self.command_prefix):
            return await super().on_message(message)
        else:
            return await on_chat_message(message)


bot = ComradeBot(command_prefix='$', intents=intents, log_handler=None)
init_commands(bot)


@bot.event
async def on_ready():
    logger.info(f'Logged on as {bot.user.name}!')


@bot.event
async def on_command_error(ctx, error):
    await ctx.send('!There is an error in your command. See $help')


@bot.event
async def on_message_delete(message: Message):
    if not is_valid_channel(message.channel):
        return

    with Session() as session:
        session.delete(
            session.query(Session).filter_by(
                message_id=message.id
            ).first()
        )
        session.commit()

    logger.info(f'Deleted message {message.id} from {message.channel.name}...')


bot.run(os.getenv('DISCORD_TOKEN'))
