import discord
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

    @commands.command()
    async def meetupmap(self, ctx: commands.context.Context):
        """Link the server\'s meetup map"""
        thumbnail = discord.File('stickers_unused/meetup_map_thumbnail.png')
        await ctx.send(content='**Gay Baby Jail Meetup Map:** https://tinyurl.com/yd9bcf7u\nIf you wish to add a marker, contact sighofrelief with your Country, City (optional), State/Providence, Description (optional), Color (optional) and Photos (optional).\nNote that if you change your discord username, people will not be able to find you from the map, and that the thumbnail may be out of date', file=thumbnail)

    @commands.command()
    @commands.has_permissions()
    async def status(self, bot):
        """Set the bot's playing status"""
        command_prefix = self.bot.command_prefix
        if bot.message.system_content == f'{command_prefix}status clear':
            await self.bot.change_presence(activity=discord.Game(f"{command_prefix}help"))
            await bot.channel.send(f"Set status to \"Playing **{command_prefix}help**\"!")
        else:
            message = bot.message.system_content.replace('!status ', '')
            await self.bot.change_presence(activity=discord.Game(f"{command_prefix}help | {message}"))
            await bot.channel.send(f"Set status to \"Playing **{command_prefix}help | {message}**\"!")

def setup(bot):
    bot.add_cog(Admin(bot))
