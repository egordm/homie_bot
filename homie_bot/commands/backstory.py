import re
from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context

from homie_bot.db import Session
from homie_bot.logging import logger
from homie_bot.models import UserInfo


class MessageContent(commands.Converter):
    async def convert(self, ctx: Context, argument):
        return re.sub(r'\$\w+\s', '', ctx.message.content)


@commands.command(help='Changes backstory for your character')
async def backstory_set(
        ctx: Context,
        backstory: str = commands.parameter(description='The backstory for your character', converter=MessageContent)
):
    backstory = backstory.strip().lstrip("\"").rstrip("\"")
    user_info = UserInfo(
        username=ctx.author.name,
        server=ctx.guild.name,
        backstory=backstory
    )

    with Session() as session:
        session.merge(user_info)
        session.commit()

    logger.info(f'Backstory set to {backstory} for {ctx.author.name}...')


@commands.command(help='View the backstory for a character. Yours by default.')
async def backstory(ctx: Context, member: Optional[discord.Member]):
    username: str = member.name if member else ctx.author.name

    with Session() as session:
        user_info = session.query(UserInfo).filter_by(
            username=username,
            server=ctx.guild.name
        ).first()

    logger.info(f'Backstory retrieved for {ctx.author.name}...')

    nickname: str = (member.nick or member.global_name or member.name) if member else 'Your'
    if user_info:
        await ctx.send(f'!{nickname} backstory is: {user_info.backstory}')
    else:
        await ctx.send(f'!{nickname} do not have a backstory set. Use $backstory_set to set one.')

