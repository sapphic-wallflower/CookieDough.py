import random

from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["flip", "coinflip", "flipcoin"])
    async def coin(self, ctx, *args):
        """Randomly selects Heads/Tails"""
        result = random.choice(['Heads', 'Tails'])
        await ctx.send(f'<@{ctx.author.id}> You got **{result}**!')

    @commands.command(aliases=["dice"])
    async def roll(self, ctx, *args):
        """Randomly selects a number in from 1 to 6"""
        result = random.choice(['1', '2', '3', '4', '5', '6'])
        await ctx.send(f'<@{ctx.author.id}> You got **{result}**!:game_die:')

    @commands.command(aliases=["8ball", "8_ball","eight_ball", "fortune_cookie"])
    async def fortune(self, ctx, *args):
        """Fortune Cookies, baked in Cookie Dough's Kitchen"""
        # 8 ball balance is based on how many replies there are. Currently there are
        # 10 yes, 2 try again, 3 chat decides, and 5 no. meaning that yes has 1/2 chance, and no has 1/4 chance.
        CHOICES_8BALL = [
            'Yepperoony!', 'Absoltutely!', 'For sure!!',
            'Yes - definitely!', 'Without a doubt!', 'uh-huh!',
            'Duh, of course!', 'I think so, yeah!', 'Yes!', 'That\'s silly, so yes!',
            'I\'m having a bit of trouble thinking right this moment... sorry', 'It\'s probably best not to tell you now :x',
            'I\'m not so sure... One of your friends here may be, though!',
            'Not sure, ask another one of your friends!',
            'Can\'t tell, but the next person other than you to say something about it will be right!',
            'Hmm... Nope!', 'I don\'t think so, no', 'Absolutely not!',
            'Sounds Silly... nah!', 'Not a chance!'
        ]
        result = random.choice(CHOICES_8BALL)
        await ctx.send(f'<@{ctx.author.id}> {result} :fortune_cookie:')

def setup(bot):
    bot.add_cog(Fun(bot))
