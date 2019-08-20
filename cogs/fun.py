import random

from discord.ext import commands

CHOICES_8BALL = [
    'It is certain.', 'It is decidedly so.', 'Without a doubt.',
    'Yes - definitely', 'You may rely on it.', 'As I see it, yes ',
    'Most likely ', 'Outlook good.', 'Yes ', 'Signs point to yes.',
    'Reply hazy, try again later ', 'Better not tell you now ',
    'I\'m not so sure...Someone else here may be, however.',
    'Answers lie within those other than me or you.Chat knows best.',
    'Methinks the next person to say something about it is correct.',
    'Don\'t count on it.', 'My reply is no.', 'My sources say no.',
    'Outlook not so good.', 'Very Doubtful.'
]


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def coin(self, ctx, *args):
        """Randomly selects Heads/Tails"""
        result = random.choice(['Heads', 'Tails'])
        await ctx.send(f'<@{ctx.author.id}> You got **{result}**!')

    @commands.command()
    async def roll(self, ctx, *args):
        """Randomly selects a number in [1, 6]"""
        result = random.choice(['1', '2', '3', '4', '5', '6'])
        await ctx.send(f'<@{ctx.author.id}> You got {result}!')

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *args):
        """The magic 8ball knows all"""

        # 8 ball balance is based on how many replies there are. Currently there are
        # 10 yes, 2 try again, 3 chat decides, and 5 no. meaning that yes has 1/2 chance, and no has 1/4 chance.
        # That is, with chat and re-rolls not counting.

        result = random.choice(CHOICES_8BALL)
        await ctx.send(f'<@{ctx.author.id}> {result} :8ball:')


def setup(bot):
    bot.add_cog(Fun(bot))
