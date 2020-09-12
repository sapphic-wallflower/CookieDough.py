import random
from discord.ext import commands
import discord
import asyncio
import logging

log = logging.getLogger("cogs.main")

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

    @commands.command(aliases=["8ball", "8_ball", "eight_ball", "fortune_cookie"])
    async def fortune(self, ctx, *args):
        """Fortune Cookies, baked in Cookie Dough's Kitchen"""
        # 8 ball balance is based on how many replies there are. Currently there are
        # 10 yes, 2 y'know/you decide, 3 chat decides, and 5 no. meaning that yes has 1/2 chance, and no has 1/4 chance.
        # We should rework this to allow for more dynamic responses. Such as one where cookie instills democracy
        #      and reacts with options for chat to vote on
        if ctx.me.permissions_in(ctx.channel).external_emojis is False:
            star_giggle = None
            qt_wink = None
        else:
            star_giggle = '<:StarGiggle:445043444805795860>'
            qt_wink = '<:QtWink:639512243796705290>'
        choices_8ball = [
            'Yepperoony!', 'Absoltutely!', 'For sure!!',
            'Yes - definitely!', 'Without a doubt!', 'uh-huh!',
            'Duh, of course!', 'I think so, yeah!', 'Yes!', 'That\'s silly, so yes!',
            f'{star_giggle} I think you already know the answer!',
            f'{qt_wink} You\'ve been good, so you can decide this time, little one!',
            'I\'m not so sure... One of your friends here may be, though!',
            'Not sure, ask another one of your friends!',
            f'first person to answer but you will decide!',
            'Hmm... Nope!', 'I don\'t think so, no', 'Absolutely not!',
            'Sounds Silly... nah!', 'Not a chance!'
        ]
        result = random.choice(choices_8ball)
        await ctx.send(f'<@{ctx.author.id}> {result} :fortune_cookie:')

    @commands.command(aliases=["rps"])
    async def rockpaperscissors(self, ctx):
        """Play a game of Rock Paper Scissors against an opponent or against Cookie Dough."""
        if ctx.me.permissions_in(ctx.channel).add_reactions is False:
            ctx.send('Hey, I need permission to add reactions in order to run this game!')
            return
        if ctx.me.permissions_in(ctx.channel).external_emojis is False:
            emoji_set = {'yes': '👍', 'no': '👎',
                         'rock': '✊',
                         'paper': '✋',
                         'scissors': '✌'}
        else:
            emoji_set = {'yes': '👍', 'no': '👎',
                         'rock': '<:rock:753111611740258305>',
                         'paper': '<:paper:753111606090661949>',
                         'scissors': '✂️'}

        emoji_yes = emoji_set['yes']
        emoji_no = emoji_set['no']
        emojis_yesno = (emoji_yes, emoji_no)
        emoji_rock = emoji_set['rock']
        emoji_paper = emoji_set['paper']
        emoji_scissors = emoji_set['scissors']
        emojis_rps = (emoji_rock, emoji_paper, emoji_scissors)

        if len(ctx.message.mentions) is not 1 or ctx.message.mentions[0].mention == ctx.author.mention:
            await ctx.send('Please @mention someone other than yourself that you\'d like to play with! \
(Only one opponent at a time please)')
            return
        else:
            player1 = ctx.author
            player2 = ctx.message.mentions[0]
            challenge = await ctx.send(f'{player2.mention} would you like to play {player1.mention} in a game of rock \
paper scissors?')
            await asyncio.gather(
                challenge.add_reaction(emoji_yes),
                challenge.add_reaction(emoji_no)
            )

            def chose_yesno(reaction, user):
                return reaction.message.id == challenge.id and user.id == player2.id \
                       and (str(reaction.emoji) in emojis_yesno)

            try:
                reaction_confirm, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=chose_yesno)
            except asyncio.TimeoutError:
                await ctx.channel.send(f'Oops, I didn\'t get a response from {player2.name}.')
                return
            if str(reaction_confirm.emoji) == emoji_no:
                await ctx.channel.send(f'{player2.mention} has declined to battle with you, {player1.mention}')
                return

            async def send_check(player, opponent):
                message = await player.send(f'Would you like to use {emoji_rock}, \
{emoji_paper}, or {emoji_scissors} against {opponent.mention}?')

                await asyncio.gather(*[
                    message.add_reaction(emoji) for emoji in emojis_rps
                ])
                return message

            # Send out the checks to DMs and notify players with the link to them
            p1game, p2game = await asyncio.gather(send_check(player1, player2), send_check(player2, player1))
            await ctx.channel.send(f'Here\'s some quick links to my DM so you can make your choices! \n\
{player1.mention}: {p1game.jump_url}\n{player2.mention}: {p2game.jump_url}')

            async def battle_check(player, message: discord.Message):
                def chose_rps(reaction, user):
                    return reaction.message.id == message.id and user.id == player.id \
                           and str(reaction.emoji) in emojis_rps

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=chose_rps)
                except asyncio.TimeoutError:
                    await ctx.channel.send(f'Oops, I didn\'t get a response from {player.name}. Try Again!')
                    return None
                await message.edit(content=f'You chose {reaction.emoji}.\nReturn link: {challenge.jump_url}')
                await ctx.channel.send(f'{player.name} responded {reaction.emoji}')
                return str(reaction.emoji)

            # Wait for responses (or non-responses)
            p1response, p2response = await asyncio.gather(battle_check(player1, p1game), battle_check(player2, p2game))

            # Do stuff with the responses here
            # probably should have the reponse message send after both players have chosen instead of above


def setup(bot):
    bot.add_cog(Fun(bot))
