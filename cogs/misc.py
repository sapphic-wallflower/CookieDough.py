import discord
from discord.ext import commands

class misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def meetupmap(self, ctx: commands.context.Context):
        """Link the server\'s meetup map"""
        thumbnail = discord.File('stickers_unused/meetup_map_thumbnail.png')
        await ctx.send(
            content='**Gay Baby Jail Meetup Map:** https://tinyurl.com/yd9bcf7u\nIf you wish to add a marker, contact Sigh with your Country, City (optional), State/Providence, Description (optional), Color (optional) and Photos (optional).\nNote that if you change your discord username, people will not be able to find you from the map, and that the thumbnail may be out of date',
            file=thumbnail)


def setup(bot):
    bot.add_cog(misc(bot))