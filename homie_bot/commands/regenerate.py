from discord.ext import commands
from discord.ext.commands import Context

from homie_bot.commands.chat import chat
from homie_bot.logging import logger


@commands.command(
    help='Regenerates last message in the channel.'
)
async def regenerate(
        ctx: Context,
):
    await ctx.channel.purge(limit=2)
    logger.info(f'Regenerating {ctx.channel.name}...')
    await chat(ctx.message)

