import logging
from discord import MessageType, Embed, Webhook, AsyncWebhookAdapter
from discord.ext import commands
import aiohttp
import asyncio

log = logging.getLogger("cogs.testing")


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """When a user reacts to a message, ping the user, link the message, and post the reacted emoji"""
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reactor = self.bot.get_user(payload.user_id)
        if payload.emoji.name == 'blueone':
            destination_name = 'general'
        elif payload.emoji.name == 'redtwo':
            destination_name = 'general-2'
        else:
            return

        wh_info_found = None
        for wh_info in await message.guild.webhooks():
            if wh_info.channel.name == destination_name:
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
            if reactor.color.value == 0x000000:
                embdcolor = 0xb9bbbe
            else:
                embdcolor = reactor.color

            enbd = Embed(
                description=f'[Jump To Original Message!]({message.jump_url})\n(from <#{channel.id}>)\n{reactor.mention} wants to talk about this:',
                color=embdcolor)
            if len(message.embeds) > 0:

                if message.embeds[0].type == 'video':
                    enbd.set_image(url=f'{message.embeds[0].thumbnail.url}')
                    enbd.add_field(name='This pin has a video! :movie_camera:',
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
                        enbd.add_field(name='This pin has a video! :movie_camera:',
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
                        enbd.add_field(name='This pin has a video! :movie_camera:',
                                       value=f'[Jump]({message.jump_url}) to watch!',
                                       inline=False)
                else:
                    if len(message.embeds[0].image) > 0:
                        enbd.set_image(url=message.embeds[0].image.url)
                    elif len(message.embeds[0].thumbnail) > 0:
                        enbd.set_image(url=message.embeds[0].thumbnail.url)
                        enbd.add_field(name='This pin may have a video! :movie_camera:',
                                       value=f'[Jump]({message.jump_url}) to watch!',
                                       inline=False)
                    enbd.add_field(name='** **',
                                   value=f'**{message.embeds[0].title}**\n{message.embeds[0].description}',
                                   inline=False)

            if len(message.attachments) > 0:
                if message.attachments[0].filename.endswith(('.png', '.jpg', '.gif', '.jpeg', '.webp')):
                    enbd.set_image(url=f'{message.attachments[0].url}')

                elif message.attachments[0].filename.endswith(('.mp4', '.webm')):
                    enbd.set_image(
                        url=f'{message.attachments[0].proxy_url}?format=jpeg&width={message.attachments[0].width}&height={message.attachments[0].height}')
                    enbd.add_field(name='This pin could have a video! :movie_camera:',
                                   value=f'[Jump]({message.jump_url}) to watch!',
                                   inline=False)

                elif message.attachments[0].filename.endswith('.mp3'):
                    enbd.add_field(name='This pin has a sound file! :musical_note:',
                                   value=f'**{message.attachments[0].filename}**\n[Jump]({message.jump_url}) to listen!',
                                   inline=False)

                else:
                    enbd.add_field(name=f'This pin has an unembeddable file! :dividers:',
                                   value=f'**{message.attachments[0].filename}**\n[Jump]({message.jump_url}) to see it!',
                                   inline=False)

            if len(message.embeds) + len(message.attachments) > 1:
                enbd.add_field(name='This Pin Has _**Multiple Files**_ :dividers:',
                               value=f'[Jump]({message.jump_url}) to see all of them!',
                               inline=False)

            if len(message.content) > 0:
                enbd.add_field(name='** **', value=f'{message.content}')
            enbd.set_footer(text=f'Originally Posted by {message.author}', icon_url=f'{message.author.avatar_url}')

            await webhook.send(avatar_url=f'{reactor.avatar_url}',
                               username=reactor.display_name,
                               embed=enbd)

            blueone = None
            redtwo = None
            for reaction in message.reactions:
                if reaction.emoji.name == "blueone":
                    blueone = reaction
                if reaction.emoji.name == "redtwo":
                    redtwo = reaction
            if payload.emoji.name == 'blueone':
                await message.remove_reaction(emoji=blueone, member=reactor)
            if payload.emoji.name == 'redtwo':
                await message.remove_reaction(emoji=redtwo, member=reactor)

            await channel.send(f'{reactor.mention} Moved It to <#{wh_info_found.channel_id}>!', delete_after=3)
def setup(bot):
    bot.add_cog(Testing(bot))
