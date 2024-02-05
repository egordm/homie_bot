from discord.ext.commands import Bot

from .lore import *
from .regenerate import regenerate
from .reset import reset
from .purge import purge
from .backstory import backstory_set, backstory


def init_commands(bot: Bot):
    bot.add_command(reset)
    bot.add_command(purge)
    bot.add_command(backstory_set)
    bot.add_command(backstory)

    bot.add_command(lore_add)
    bot.add_command(lore_view)
    bot.add_command(lore_delete)
    bot.add_command(lore_list)

    bot.add_command(regenerate)
