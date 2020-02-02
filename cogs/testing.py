import logging
from discord.ext import commands

log = logging.getLogger("cogs.testing")


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Testing(bot))
