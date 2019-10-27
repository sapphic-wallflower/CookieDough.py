from discord.ext import commands
from discord.ext.commands import BadArgument


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx: commands.context.Context, n: int):
        """Purge `n` messages"""
        if n <= 0 or n > 49:
            raise BadArgument("n should be in [1,49]")
        deleted = await ctx.channel.purge(limit=n+1)
        reply = await ctx.send(f'{len(deleted)-1} message(s) purged')
        await reply.delete(delay=1)


def setup(bot):
    bot.add_cog(Admin(bot))
