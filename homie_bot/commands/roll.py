from typing import Optional
import random

from discord.ext import commands
from discord.ext.commands import Context

from homie_bot.commands.chat import chat
from homie_bot.logging import logger
from homie_bot.utils import format_name

SPECIAL_DIE = {20, 100}

@commands.command(
    help='Rolls a dice.'
)
async def roll(ctx: Context, number_of_sides: Optional[int] = 8):
    if number_of_sides < 2:
        logger.info(f'Invalid number of sides for dice roll: {number_of_sides}')
        await ctx.send('Invalid number of sides for dice roll.')
        return

    author = format_name(ctx.author)
    value = random.randint(1, number_of_sides)
    logger.info(f'Rolled a {number_of_sides}-sided dice for {author}...')

    if number_of_sides in SPECIAL_DIE and value == number_of_sides:
        await ctx.send(f'{author} rolled a *natural {number_of_sides}* with *d{number_of_sides}* dice!')
    elif number_of_sides in SPECIAL_DIE and value == 1:
        await ctx.send(f'{author} rolled a *critical failure* with a *d{number_of_sides}* dice!')
    else:
        await ctx.send(f'{author} rolled *{value}* with a *d{number_of_sides}* dice!')

    # Trigger chat
    await chat(ctx.message)
