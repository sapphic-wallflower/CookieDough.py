import logging
import discord
from discord import Embed, Webhook, AsyncWebhookAdapter
from discord.ext import commands
import aiohttp
# from pysaucenao import SauceNao

log = logging.getLogger("cogs.misc")

class misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def meetupmap(self, ctx: commands.context.Context):
        """Link the server\'s meetup map"""
        thumbnail = discord.File('stickers_unused/meetup_map_thumbnail.png')
        await ctx.send(
            content='**Gay Baby Jail Meetup Map:** <https://tinyurl.com/yd9bcf7u>\nIf you wish to add a marker, contact Sigh with your Country, City (optional), State/Providence, Description (optional), Color (optional) and Photos (optional).\nNote that if you change your discord username, people will not be able to find you from the map, and that the thumbnail may be out of date',
            file=thumbnail)

    @commands.command(aliases=["donations", "support"])
    async def donate(self, ctx: commands.context.Context):
        """server's donation link"""
        thumbnail = discord.File('stickers/cardboard_banner.png')
        await ctx.send(
            content='**Gay Baby Jail Donation Link:** https://www.abdlgaybabyjail.org/donations\n If you like the server and want to support it\'s creator,\
 click here to donate! Be sure to check out our reward tiers and goals!',
            file=thumbnail)

    @commands.command(aliases=["diaplist"])
    async def diaperlist(self, ctx: commands.context.Context):
        """Amazon Affiliate Diaper List"""
        await ctx.send('**Every ABDL Diaper on Amazon:** https://amzn.to/2tueosG \nNote that this is an affiliate link, so Gay Baby Jail may get kickback on applicable items.')

    @commands.command(aliases=["plasticlist"])
    async def clothlist(self, ctx: commands.context.Context):
        """Amazon Affiliate Cloth and Plastic Diaper List"""
        await ctx.send(
            '**Plastic Pants and Cloth Diapers:** https://amzn.to/2PDQKCE \nNote that this is an affiliate link, so Gay Baby Jail may get kickback on applicable items.')

    @commands.command(aliases=["pacilist", "accessorieslist"])
    async def accessorylist(self, ctx: commands.context.Context):
        """Amazon Affiliate Accessory List"""
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

   # @commands.command()
    #async def SauceNao(self):
    #    sauce = SauceNao()
    #    image_url = None

        # results = await sauce.from_file('/path/to/image.png')
     #   results = await sauce.from_url(f'{image_url}')
    #    repr(results)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send('https://cdn.discordapp.com/attachments/610127221855748096/661396909264601089/Welcome.gif')
        await member.send(f'Hey there! <:MeruWave:659291486793498634> Welcome to **{member.guild.name}**! Please take \
a look at our rules and info! Then when you\'re ready, please ping OB/GYN with your age and how you heard about us! \
<:MeruPaci:430485696193757184> Oh, and please be patient after doing so, a human moderator will let you in as soon as \
they can!')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """when a user reacts to a message with specific emoji, embed that message in another channel"""
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reactor_id = self.bot.get_user(payload.user_id)
        reactor_member = payload.member

        if message.channel.type.name is 'private' or channel.name.find('media') is -1:  # looks for the position of substring. if it's not found, this returns -1.
            return
        if payload.emoji.name == 'MoveToGeneral':
            destination_name = 'general💖'
        elif payload.emoji.name == 'MoveToDiaperChat':
            destination_name = 'diaper-chat🧸'
        else:
            return

        wh_info_found = None
        for wh_info in await message.guild.webhooks():
            if wh_info.channel.name == destination_name and wh_info.token is not None:
                wh_info_found = wh_info
                break
        if wh_info_found is None:
            await message.channel.send(
                f'Missing webhook for #{destination_name}',
                delete_after=8)
            return
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(wh_info_found.url, adapter=AsyncWebhookAdapter(session))
            if webhook is None:
                log.error(f'Unable find a webhook in the #{destination_name} channel!')
                await message.send(f'Unable find a webhook in a #{destination_name} channel!', delete_after=8)
                return
            if reactor_member.color.value == 0x000000:
                embdcolor = 0xb9bbbe
            else:
                embdcolor = reactor_member.color

            enbd = Embed(
                description=f'[Jump To Original Message!]({message.jump_url})\n(from <#{channel.id}>)\n{reactor_id.mention} wants to talk about this:',
                color=embdcolor)
            if len(message.embeds) > 0:

                if message.embeds[0].type == 'video':
                    enbd.set_image(url=f'{message.embeds[0].thumbnail.url}')
                    enbd.add_field(name='This post has a video! :movie_camera:',
                                   value=f'**{message.embeds[0].title}**\n[Jump]({message.jump_url}) to watch!',
                                   inline=False)

                elif message.embeds[0].type == 'image':
                    enbd.set_image(url=f'{message.embeds[0].thumbnail.url}')

                elif message.embeds[0].type == 'gifv':
                    if message.embeds[0].provider.name == 'Giphy':
                        enbd.set_image(url=f'{message.embeds[0].url}')
                    else:
                        enbd.set_image(url=f'{message.embeds[0].thumbnail.proxy_url}')
                    if message.embeds[0].provider.name == 'Tenor':
                        enbd.add_field(name='This post has a video! :movie_camera:',
                                       value=f'[Jump]({message.jump_url}) to watch!',
                                       inline=False)

                elif message.embeds[0].type == 'rich':
                    enbd.add_field(name='** **',
                                   value=f'[{message.embeds[0].author.name}]({message.embeds[0].author.url})\n{message.embeds[0].description}',
                                   inline=False)
                    if len(message.embeds[0].image) > 0:
                        enbd.set_image(url=message.embeds[0].image.url)
                    elif len(message.embeds[0].thumbnail) > 0:
                        enbd.set_image(url=message.embeds[0].thumbnail.url)
                        enbd.add_field(name='This post has a video! :movie_camera:',
                                       value=f'[Jump]({message.jump_url}) to watch!',
                                       inline=False)
                else:
                    if len(message.embeds[0].image) > 0:
                        enbd.set_image(url=message.embeds[0].image.url)
                    elif len(message.embeds[0].thumbnail) > 0:
                        enbd.set_image(url=message.embeds[0].thumbnail.url)
                        enbd.add_field(name='This post may have a video! :movie_camera:',
                                       value=f'[Jump]({message.jump_url}) to watch!',
                                       inline=False)
                    enbd.add_field(name='** **',
                                   value=f'**{message.embeds[0].title}**\n{message.embeds[0].description}',
                                   inline=False)

            if len(message.attachments) > 0:
                if message.attachments[0].filename.endswith(('.png', '.jpg', '.gif', '.jpeg', '.webp')):
                    enbd.set_image(url=f'{message.attachments[0].url}')

                elif message.attachments[0].filename.endswith(('.mp4', '.webm', '.mov')):
                    enbd.set_image(
                        url=f'{message.attachments[0].proxy_url}?format=jpeg&width={message.attachments[0].width}&height={message.attachments[0].height}')
                    enbd.add_field(name='This post could have a video! :movie_camera:',
                                   value=f'[Jump]({message.jump_url}) to watch!',
                                   inline=False)

                elif message.attachments[0].filename.endswith('.mp3'):
                    enbd.add_field(name='This post has a sound file! :musical_note:',
                                   value=f'**{message.attachments[0].filename}**\n[Jump]({message.jump_url}) to listen!',
                                   inline=False)

                else:
                    enbd.add_field(name=f'This post has an unembeddable file! :dividers:',
                                   value=f'**{message.attachments[0].filename}**\n[Jump]({message.jump_url}) to see it!',
                                   inline=False)

            if len(message.embeds) + len(message.attachments) > 1:
                enbd.add_field(name='This post Has _**Multiple Files**_ :dividers:',
                               value=f'[Jump]({message.jump_url}) to see all of them!',
                               inline=False)

            if len(message.content) > 0:
                enbd.add_field(name='** **', value=f'{message.content}')
            enbd.set_footer(text=f'Originally Posted by {message.author}', icon_url=f'{message.author.avatar_url}')

            await webhook.send(avatar_url=f'{reactor_id.avatar_url}',
                               username=reactor_id.display_name,
                               embed=enbd)

            movetogeneral = None
            movetodiaperchat = None
            for reaction in message.reactions:
                if not reaction.custom_emoji:
                    continue
                if reaction.emoji.name == "MoveToGeneral":
                    movetogeneral = reaction
                if reaction.emoji.name == "MoveToDiaperChat":
                    movetodiaperchat = reaction
            if payload.emoji.name == 'MoveToGeneral':
                await message.clear_reaction(emoji=movetogeneral)
            if payload.emoji.name == 'MoveToDiaperChat':
                await message.clear_reaction(emoji=movetodiaperchat)

            await channel.send(f'{reactor_id.mention} Moved It to <#{wh_info_found.channel_id}>!', delete_after=3)

def setup(bot):
    bot.add_cog(misc(bot))
