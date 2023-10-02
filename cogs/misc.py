import logging
from discord.ext import commands

log = logging.getLogger("cogs.misc")

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def faq(self, ctx):
        """FAQ/Copypasta list"""
        await ctx.message.delete()
        await ctx.send('''
## Gay Baby Jail - Frequently Asked Questions
Below is a list of commands you can use to either learn more about the server or quickly educate others
* Roles and Economy: `.economy`, `.allroles`, `.diapertraining`
* Bots: `.pluralkit`, `.modmail`, `.help`, `pk;help`
* Other: `.feedback`, `.roleplay`, `.textrules`, `.lights`, `.discussion`, `.mediaguide`
''')

    @commands.command()
    async def economy(self, ctx):
        """copypasta command explaining all the ways to earn cookies in the economy"""
        await ctx.message.delete()
        await ctx.send('''
## Earning Cookies🍪:
* Use `/work` or `!work`
 * You'll earn 75-125🍪. You're able to do this every eight hours.
* If you're boosting the server, use `/collect-income` or `!collectincome`
 * you'll earn 1000🍪. You can do this once a month.
* Post content in <#466529435861123072> and/or <#395817140181008394>
 * You get get 35🍪 for each 🍪 reaction on your posts in these channels.
 * If your message makes it to <#637898801352540176>, you earn 150🍪.
  * NOTE: This is done manually. If you'd like to collect your Cookies🍪, ping `@girl.kisser` in <#395837746083528704> \
with how many 🍪 reactions your posts have  or if your post was sent to <#637898801352540176>. 
* Post content in the media channels.
 * If your message gets 15 human 📌 reactions, it'll be sent to <#637898801352540176>. This will earn you 150🍪.
  * NOTE: This is done manually. If you'd like to collect your Cookies🍪, ping `@girl.kisser` in <#395837746083528704>
* Complete tasks for (or gamble with) other users in <#399280851856130050>
 * A list of tasks are posted in the pinned messages of that channel if you need some ideas.
## Spending Cookies🍪:
* Use `!store` to see what items we have available in the shop.
* Use `!buy [item name]` to buy an item from the shop.
* Use `!pay [@username] [amount]` to give Cookies🍪 to other users.
## Miscellaneous:
* Use `!bal` to check your Cookie🍪 balance. 
 * (You can also check the balance of another user by using `!bal [@ping]`)
* Use `.allroles` to see a list of all the custom roles on the server.
* Use `.help` to see a list of commands provided by me, <@!641788291225747487>!
''')

    @commands.command(aliases=["diaperserver"])
    async def discussion(self, ctx):
        """copypasta command explaining why we allow and encourage serious or adult conversations"""
        await ctx.message.delete()
        await ctx.send(
            '''Gay Baby Jail is not _just_ a diaper server. Its mostly a hangout server where diapers are normalized. \
We don't allow roleplay or baby-talk in the generals, and we're all adults. While serious topics aren't always being \
discussed, they are very much welcome in our server. Our goal is to create a kink-positive space; not a kink-only space.
Attempting to derail or discourage conversations by spamming GIFs, bringing up random topics, or exclaiming something \
to the effect of "this is a diaper server, why are we talking about this?" will result in a warning and/or a timeout.
If the current topic makes you uncomfortable, we have other channels, and there's plenty of other servers you can \
visit in the meantime as well. Thank you for your understanding.
''')

    @commands.command()
    async def modmail(self, ctx):
        """copypasta command explaining modmail"""
        await ctx.message.delete()
        await ctx.send('''\
If you'd like to reach out to the mod team, please send a Direct-Message to <@!575252669443211264> instead of our DMs.
This allows your message to be seen by all of us, which helps us to collaborate as a team on issues. As well, any mod \
that sees it can respond to it as soon as possible. Someone who's shown as online doesn't mean they're actually there, \
just as being idle doesn't mean they aren't.
ModMail also separates administrative issues from casual conversation in our DMs, which is a big help to us.
Thank you for understanding!
''')

    @commands.command(aliases=["mediaguide", "media", "mediaguidelines"])
    async def mediaguideline(self, ctx):
        """copypasta command explaining what kind of images are allowed in media channels"""
        await ctx.message.delete()
        await ctx.send('''\
Images which have the intention of being (abdl-)memes rather than "abdl-media" should be posted in \
<#639395194898219011>, and should not be posted in media channels. Posts in media channels must somehow pass as art, \
porn, photosets, erotica, fantasy, or something thereof, and must seem to have an intent to illicit either an erotic \
or aesthetic response in greater or equal proportion to memetic value. Bonus points for original art assets. You "know \
it when you see it".
[**Here's a few examples of what and what not to post in media channels (img-link)**](https://files.catbox.moe/e3vxwj.png)''')

    @commands.command(aliases=["pk"])
    async def pluralkit(self, ctx):
        """copypasta command explaining what pluralkit is"""
        await ctx.message.delete()
        await ctx.send('''
## ____Why Are There Bots Talking?____
<@!466378653216014359> is a bot designed for plural systems that use Discord. It allows you to register systems, \
maintain system information, set up alters, set up message proxying, log headmate switching, and more.
Basically, the bot detects messages from an account and then is able to replace that message under a "proxy" \
account using webhooks. This is useful for multiple people sharing one body (systems), people who wish to \
roleplay as different characters without having several accounts, or anyone else who may want to post messages as a \
different person from one account. TL;DR, they're not bots, but regular chatters proxying their messages through \
a bot. You can react to a PK proxied message with ❓ to get info about the account that posted it, and 🔔 to ping the \
account.

You can learn more about the bot on [PluralKit's website](<https://pluralkit.me/>) \
or by using `pk;help in <#395837746083528704>`
You can learn more about plurality on [MoreThanOne.info](<https://morethanone.info/>)''')

    @commands.command(aliases=["listroles", "roleslist", "rolelist"])
    async def allroles(self, ctx):
        """copypasta command that lists all available roles"""
        await ctx.message.delete()
        await ctx.send('''\
## All Custom Roles
We had to move the list to [this google sheet](<https://bit.ly/3Bd1Zbq>), it doesn't fit in discord anymore!
## Special Roles
* **<:PottyBanned:779149826154823691> Diaper Training** is a challenge role that diaperchecks you. Use \
`.diapertraining` in <#395837746083528704> for more info.\
''')

    @commands.command()
    async def diapertraining(self, ctx):
        """copypasta explaining the diapertraining role"""
        await ctx.message.delete()
        await ctx.send('''\
## <:PottyBanned:779149826154823691> What Is This?
When the Diaper Training role is pinged, all users must prove they're wearing a diaper with a picture. \
If you'd like to participate, you can buy the role in <#395837746083528704> for 3000🍪.
## 📜 Rules:
* Once pinged, you have 3 hours to prove you're padded. After you've provided proof, you're immune for 8 hours. \
However, we encourage you to continue participating.
* You can provide preemptive proof if you know you'll be unable to check discord for over 3 hours. \
When you return, you must also provide another picture.
 * You must provide a detailed explanation as to why. Mundane reasons won't be accepted.
* If asleep, you'll be required to show proof upon waking up.
## <:MeruPolice:935948597063716874> Punishment for Failure:
Failing to respect the rules will result in a 1,000🍪 penalty OR losing the role. 
To pay the fee, type `!pay <@641788291225747487> 1000` (or just pay <@!641788291225747487> 1000🍪). 
If you would rather not pay, ping `@girl.kisser` or `@Glasswalker` to remove the role.
**If you're caught lying or reusing an old photo, you will be banned from the server for 14 days.**
''')

    @commands.command(aliases=["suggest", "suggestion"])
    async def feedback(self, ctx):
        """copypasta command template"""
        await ctx.message.delete()
        await ctx.send('''\
If you'd like to submit feedback or suggestions to the server, it's bots, etc., you can use \
`?suggest [your suggestion]`. This will create a poll which is sent to <#466459060258996225>, which helps us to gauge \
interest and support.
''')

    @commands.command(aliases=["rule2", "rp"])
    async def roleplay(self, ctx):
        """copypasta command template"""
        await ctx.message.delete()
        await ctx.send('''\
## Rule 2: No Roleplay (or baby-talk)
We understand this is a very divisive rule which many don't understand. In short, we haven't curated GBJ to be a \
space for roleplay, and we feel it often comes into conflict with our desire to make the server a casual hang-out spot \
to have conversation in. There is a community owned opt-in channel <#855947209560162355> where you're free to roleplay \
and use baby-talk to your heart's content. You can opt-in at <#858253598944526337>. We also allow roleplay in \
<#1006312425487867944> threads which explicitly allow it in the OP.
\
## How does GBJ define roleplay (and baby-talk)?
We define **roleplay** in a number of ways. One of which includes any type of "action message". Examples include: \
_hugs_, [hugs], hugs you, etc.
Of course, roleplay can also involve any type of behavior which is fictional in nature and meant to act out a fantasy. \
one could roleplay a conversation with fictional circumstances. For example, talking as if you're in a nursery and are \
getting changed by the person you're talking to (or vice versa.)
Just because it isn't listed as an example doesn't mean we may not consider it roleplay. We'll use our best judgement \
when we're determining if a message is RP or not. However, emoji in almost all contexts are fine. Maybe use those as a\
substitute!
**Baby-talk** is a bit more complicated, but it's sort of a "know it when you see it" situation. Purposefully incorrect \
grammar, spelling, etc.
\
## How can I express myself?
As stated earlier, we have a range of emoji that you can use to express yourself, many of which are available without \
Nitro. If there's an emote we're missing, you can use `.economy` to learn how to buy it and add it to the server. You \
can also use `.stamps` to get a list of stamps provided by me, <@!641788291225747487>! They're a bit like stickers, but \
completely free. Albeit they only work in servers I'm a part of.
''')

    @commands.command(aliases=["rules"])
    async def textrules(self, ctx):
        """copypasta command template"""
        await ctx.message.delete()
        await ctx.send('''\
[Here's a link to our current rules in plain text]\
(https://docs.google.com/document/d/13pxzthxFImkSLBOit4u4J6QXi2_5cbVq41qcwcnBYFE). \
You can make a copy by clicking `File > Make a copy` if you need to make it more readable. 
''')

    @commands.command()
    async def lights(self, ctx):
        """copypasta command template"""
        await ctx.message.delete()
        await ctx.send('''\
## Consent Indicators (aka lights)
* <:LightGreen:749514803822854224>: All clear, everything is going well. I consent.
* <:LightYellow:749514808335925288>: No to that, but lets keep going. Or, pause and check in. Something's not working.
* <:LightRed:749514808331731034>: Stop immediately and begin aftercare.
Failure to follow or heed to people's lights will result in an immediate ban. We take consent very seriously here.
''')

async def setup(bot):
    await bot.add_cog(Misc(bot))
