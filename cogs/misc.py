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

    @commands.command(aliases=["diaplist"])
    async def diaperlist(self, ctx: commands.context.Context):
        """Amazon Affiliate diaper list"""
        await ctx.send('**Every ABDL Diaper on Amazon:** https://amzn.to/2tueosG \nNote that this is an affiliate link, so Gay Baby Jail may get kickback on applicable items.')

    @commands.command(aliases=["plasticlist"])
    async def clothlist(self, ctx: commands.context.Context):
        """Amazon Affiliate cloth and plastic diaper list"""
        await ctx.send(
            '**Plastic Pants and Cloth Diapers:** https://amzn.to/2PDQKCE \nNote that this is an affiliate link, so Gay Baby Jail may get kickback on applicable items.')

    @commands.command(aliases=["pacilist", "accessorieslist"])
    async def accessorylist(self, ctx: commands.context.Context):
        """Amazon Affiliate accessory list"""
        await ctx.send(
            '**A ton of ABDL accessories:** https://amzn.to/35MqXOA \nNote that this is an affiliate link, so Gay Baby Jail may get kickback on applicable items.')

    @commands.command(aliases=["onesielist", "dresseslist", "dresslist"])
    async def outfitlist(self, ctx: commands.context.Context):
        """Amazon Affiliate Onesies, Outfits, and Dresses"""
        await ctx.send(
            '**Onesies, Outfits, and Dresses:** https://amzn.to/2Q6RIX0 \nNote that this is an affiliate link, so Gay Baby Jail may get kickback on applicable items.')

    @commands.command(aliases=["stuffylist"])
    async def stuffielist(self, ctx: commands.context.Context):
        """Amazon Affiliate Stuffie list"""
        await ctx.send(
            '**Stuffie list:** https://amzn.to/2Q7oac9 \nNote that this is an affiliate link, so Gay Baby Jail may get kickback on applicable items.')
def setup(bot):
    bot.add_cog(misc(bot))