from discord.ext import commands
from discord.ext.commands import Context

from homie_bot.db import Session
from homie_bot.logging import logger
from homie_bot.models import Lore

__all__ = ['lore_add', 'lore_view', 'lore_delete', 'lore_list']


@commands.command(help='Creates a lore entry')
async def lore_add(
        ctx: Context,
        names: str = commands.parameter(description='The names by which lore is invoked'),
        content: str = commands.parameter(description='The content of the lore')
):
    names = names.strip()
    content = content.strip()
    lore = Lore(
        server=ctx.guild.name,
        channel=ctx.channel.name,
        names=names,
        content=content
    )

    with Session() as session:
        session.merge(lore)
        session.commit()

    logger.info(f'Lore added for {names} in {ctx.guild.name}...')
    await ctx.send(f'!Lore added for {names} in {ctx.guild.name}...')


@commands.command(help='View a lore entry')
async def lore_view(
        ctx: Context,
        names: str = commands.parameter(description='The names by which lore is invoked')
):
    names = names.strip()

    with Session() as session:
        lore = session.query(Lore).filter_by(
            names=names,
            server=ctx.guild.name,
            channel=ctx.channel.name
        ).first()

    logger.info(f'Lore retrieved for {names} in {ctx.guild.name}...')

    if lore:
        await ctx.send(f'!Lore for {names} is: {lore.content}')
    else:
        await ctx.send(f'!Lore for {names} does not exist in {ctx.guild.name}...')


@commands.command(help='Deletes a lore entry')
async def lore_delete(
        ctx: Context,
        names: str = commands.parameter(description='The names by which lore is invoked')
):
    names = names.strip()

    with Session() as session:
        lore = session.query(Lore).filter_by(
            names=names,
            server=ctx.guild.name,
            channel=ctx.channel.name
        ).first()

        if lore:
            session.delete(lore)
            session.commit()
            logger.info(f'Lore deleted for {names} in {ctx.guild.name}...')
            await ctx.send(f'!Lore deleted for {names} in {ctx.guild.name}...')
        else:
            logger.info(f'Lore for {names} does not exist in {ctx.guild.name}...')
            await ctx.send(f'!Lore for {names} does not exist in {ctx.guild.name}...')

    logger.info(f'Lore deleted for {names} in {ctx.guild.name}...')
    await ctx.send(f'!Lore deleted for {names} in {ctx.guild.name}...')


@commands.command(help='Lists all lore entries')
async def lore_list(ctx: Context):
    with Session() as session:
        lore = session.query(Lore).filter_by(
            server=ctx.guild.name,
            channel=ctx.channel.name
        ).all()

    logger.info(f'Lore list retrieved for {ctx.guild.name}...')

    text = ''
    for l in lore:
        text += f'**{l.names}**: {l.content}\n\n'

    if lore:
        await ctx.send(f'!Lore entries in {ctx.guild.name} are:\n{text}')
    else:
        await ctx.send(f'!No lore entries in {ctx.guild.name}...')
