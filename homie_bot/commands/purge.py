from discord.ext import commands
from discord.ext.commands import Context

from homie_bot.logging import logger


@commands.command(
    help='Purge n messages from the channel'
)
async def purge(
        ctx: Context,
        n: int = commands.parameter(description='The number of messages to purge', default=5)
):
    await ctx.channel.purge(limit=n)
    logger.info(f'Purged {n} messages from {ctx.channel.name}...')
    await ctx.send(f'!Purged {n} messages from {ctx.channel.name}...')

