import logging
from discord.ext import commands

log = logging.getLogger("cogs.misc")

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["diaperserver"])
    async def discussion(self, ctx):
        """copypasta command explaining why we allow and encourage serious or adult conversations"""
        await ctx.message.delete()
        await ctx.send(
            'Gay Baby Jail is not _just_ a diaper server. It\'s mostly a hangout server where diapers are normalized. \
We don\'t allow roleplay, we don\'t allow baby-talk, and we\'re all adults. While serious topics aren\'t always being \
discussed, they are **very much** welcome in our server.\n\n\
Attempting to derail or discourage conversations by \
spamming GIFs, bringing up random topics, or exclaiming that "this is a diaper server, why are we talking about this" \
will result in a warning and/or a timeout.\n\n\
If it makes you uncomfortable to be around these topics, we have other \
channels, and there\'s even other servers you can use in the meantime while the discussion is happening. Thanks \
for your understanding.')

    @commands.command()
    async def mediaguideline(self, ctx):
        """copypasta command explaining what kind of images are allowed in media channels"""
        await ctx.message.delete()
        await ctx.send('Images which don\'t have the intention of being \"abdl-media\" but being memes or jokes should \
be posted in <#639395194898219011>, and should not be posted in media channels (<#1007454416477110273> is an exception, \
as everything hypnosis related should stay in the hypnosis category) Posts in media channels must somehow pass as art, \
porn, photosets, erotica, fantasy, or something thereof, and must seem to have an intent to illicit either an erotic \
or aesthetic reaction in greater or equal proportion to memetic value, bonus points for original art assets. You "know \
it when you see it". Pictured are a few examples of what to and not to post in media channels. \n https://files.catbox.moe/e3vxwj.png')


async def setup(bot):
    await bot.add_cog(Misc(bot))
