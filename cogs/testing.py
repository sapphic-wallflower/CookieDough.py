import logging
from discord import MessageType, Embed
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

log = logging.getLogger("cogs.testing")


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """When a user reacts to a message, ping the user, link the message, and post the reacted emoji"""
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = self.bot.get_user(payload.user_id)
        if payload.emoji.id is None:
            emoji = payload.emoji.name
        else:
            emoji = f'<:{payload.emoji.name}:{payload.emoji.id}>'
        await channel.send(f'{user.mention} Reacted to {message.jump_url} with {emoji}!')


    @commands.command()
    async def FwiendReadPermission(self, ctx):
        """Check if the Fwiend Role can read messages in the channel that the command is used in"""
        for role in ctx.guild.roles:
            if role.name.lower() == "fwiend":
                Fwiend = role
        if ctx.channel.overwrites_for(Fwiend).read_messages is None:
            await ctx.send('Fwiend Read Permission for this channel is set to: None')
        else:
            await ctx.send(f'Fwiend Read Permission for this channel is set to: {ctx.channel.overwrites_for(Fwiend).read_messages}')

    @commands.command()
    async def webtest(self, ctx):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                'https://discordapp.com/api/webhooks/618452978655035403/hcxP1sYd2tLKYl_bmWI5iWgya-OKv8yS6zdGdjlrjo01yrR4Qx8H0qGB7YATx5iYPJNX',
                adapter=AsyncWebhookAdapter(session))
            # implimentation to automatically pull webhook url is needed
            enbd = Embed(title='Still Alive',
                         description='I\'m making a note here; **_huge success_**',
                         color=0xffaaff,
                         url='https://www.youtube.com/watch?v=Y6ljFaKRTrI')
            enbd.set_author(name='GLaDOS', url='https://theportalwiki.com/wiki/GLaDOS',
                            icon_url='https://i.imgur.com/FYckawU.png')
            enbd.set_image(
                url='https://cdn.sallysbakingaddiction.com/wp-content/uploads/2013/04/triple-chocolate-cake-4-600x900.jpg')
            enbd.set_thumbnail(
                url='https://www.healthline.com/hlcmsresource/images/topic_centers/732x549_How_to_Identify_and_Treat_Nail_Pitting.jpg')
            enbd.set_footer(text='footer text',
                            icon_url='https://footsolutions.com/wp-content/uploads/2015/09/top-foot.jpg')
            enbd.add_field(name='You are', value='Dead', inline=True)
            enbd.add_field(name='I am', value='Still Alive', inline=True)
            enbd.add_field(name='Aperture', value='Science', inline=False)
            enbd.add_field(name='We do what we must', value='because we can', inline=False)
            await webhook.send(avatar_url=f'{ctx.author.avatar_url}',
                               username=f'{ctx.author.nick}',
                               embed=enbd)

def setup(bot):
    bot.add_cog(Testing(bot))
