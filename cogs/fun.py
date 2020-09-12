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





    # @commands.command(aliases=["dice"])
    # async def roll1(self, ctx, *args):
    #     """Randomly selects a number in from 1 to 6"""
    #     result = random.choice(['1', '2', '3', '4', '5', '6'])
    #     await ctx.send(f'<@{ctx.author.id}> You got **{result}**!:game_die:')

    @commands.command(aliases=["dice"])
    async def roll(self, ctx, sides="6", num="1"):
        """Rolls dice.
        .roll - roll a 6 sided die
        .roll 6 2 - roll 2 6-sided dice
        .roll d6 2 - roll 2 6-sided dice
        .roll 2 d6 - roll 2 6-sided dice"""
        # sanitize inputs so .roll d20 works
        if sides[0] == 'd' or sides[0] == 'D':
            sides = sides[1:]
        elif num[0] == 'd' or num[0] == 'D':
            num = num[1:]
            swap = num
            num = sides
            sides = swap
        if not num.isdigit():
            num = "1"
        if not sides.isdigit():
            await ctx.send(f'<@{ctx.author.id}> I\'m not sure i get it... <:MeruSad:633650580660682762> \
Could you try it like this? <:QuestionBun:588539387688517642> \n\
`.roll d[number of sides] [number of dice]`')
        elif int(sides) == 0 or int(num) == 0:
            await ctx.send(f'<@{ctx.author.id}> Have you ever tried dividing by 0? This is a lot like that. '
                           f'Try rolling more dice next time, sweetie~ <:StarGiggle:445043444805795860>')
        else:
            sides = int(sides)
            # MAX NUMBER OF SIDES
            if sides > 1000:
                sides = 1000
                await ctx.send('that\'s a lot... let\'s go with 1000 sides per die')
            num = int(num)
            # MAX NUMBER OF DICE
            if num > 50:
                num = 50
            result = []
            for x in range(int(num)):
                result.append(str(random.randrange(sides) + 1))
            output = ", ".join(result)
            await ctx.send(f'<@{ctx.author.id}> You got **{output}**!:game_die:')


    @commands.command(aliases=["8ball", "8_ball","eight_ball", "fortune_cookie"])
    async def fortune(self, ctx, *args):
        """Fortune Cookies, baked in Cookie Dough's Kitchen"""
        # 8 ball balance is based on how many replies there are. Currently there are
        # 10 yes, 2 y'know/you decide, 3 chat decides, and 5 no. meaning that yes has 1/2 chance, and no has 1/4 chance.
        # We should rework this to allow for more dynamic responses. Such as one where cookie instills democracy
        #      and reacts with options for chat to vote on
        CHOICES_8BALL = [
            'Yepperoony!', 'Absoltutely!', 'For sure!!',
            'Yes - definitely!', 'Without a doubt!', 'uh-huh!',
            'Duh, of course!', 'I think so, yeah!', 'Yes!', 'That\'s silly, so yes!',
            '<:StarGiggle:445043444805795860> I think you already know the answer!',
            '<:QtWink:639512243796705290> You\'ve been good, so you can decide this time, little one',
            'I\'m not so sure... One of your friends here may be, though!',
            'Not sure, ask another one of your friends!',
            f'first person to answer but you will decide!',
            'Hmm... Nope!', 'I don\'t think so, no', 'Absolutely not!',
            'Sounds Silly... nah!', 'Not a chance!'
        ]
        result = random.choice(CHOICES_8BALL)
        await ctx.send(f'<@{ctx.author.id}> {result} :fortune_cookie:')


def setup(bot):
    bot.add_cog(Fun(bot))
