from typing import Optional

from discord.ext import commands
from discord.ext.commands import Context

from homie_bot.logging import logger


@commands.command(
    help='Resets the bot memory. All messages before this command will be forgotten.'
)
async def reset(ctx: Context, arg: Optional[str] = None):
    logger.info(f'Bot memory reset for {ctx.guild.name}...')
    await ctx.send('!I have forgotten everything before this message.')
