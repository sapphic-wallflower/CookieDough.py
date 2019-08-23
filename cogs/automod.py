import logging

from discord.ext import commands

log = logging.getLogger("cogs.automod")


class AutoMod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(AutoMod(bot))
