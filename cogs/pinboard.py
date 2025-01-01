import logging
import aiohttp
import asyncio
import time
import discord
from discord import MessageType, ChannelType, Embed, Webhook
from discord.ext import commands


log = logging.getLogger("cogs.pinboard")


class Pinboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload,):
        n = 15
        f"""auto-pin messages after {n} human 📌 reactions"""
        if message.type == MessageType.pins_add: #ignore [user] pinned a message server messages
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        for reaction in message.reactions:
            if reaction.emoji == '📌':
                # reaction.me checks if bot reacted, if False that means the message has already been pinned and should return.
                if reaction.count == n+1 and reaction.me:
                    await reaction.remove(self.bot.user)
                    if time.time() - message.created_at.timestamp() > 7889399: # 7889399 being 3 months in seconds
                        return
                    await message.pin()
                    log.info(f'bot pinned a message because of {reaction.count} 📌 reactions on message')
                if reaction.count == 1 and reaction.me is False:
                    await message.add_reaction('📌')  # allows cookie to add pushpin emoji to non-media message if a user reacts first
                    log.info('added a 📌 reaction to a non-media message since someone else did first')
                return

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """When a message is pinned, push an embed of that message through a webhook"""

        if message.channel.name.find('pinboard') > -1 and message.author != discord.Member: #publish the message if its a webhook message in #pinboard
            await message.publish()

        if message.type != MessageType.pins_add:
            return
        everyone = None
        fwiend = None
        for role in message.guild.roles:
            if role.name.lower() == "@everyone":
                everyone = role
            if role.name.lower() == "fwiend":
                fwiend = role
        perms_channel = message.channel.parent if isinstance(message.channel, discord.Thread) else message.channel
        ovr_everyone = perms_channel.overwrites_for(everyone).read_messages if everyone is not None else None
        ovr_fwiend = perms_channel.overwrites_for(fwiend).read_messages if fwiend is not None else None
        pinboard_name = None
        if ovr_everyone is False or ovr_fwiend is False:  # skip if the channel is private
            pass
        else:  # pinned msg is in public channel, so we'll define the name of the channel it goes to
            pinboard_name = '📌pinboard'
        if pinboard_name is None:
            await message.channel.send(
                '(btw, either @Everyone or Fwiends can\'t see this channel. So I can\'t put that message on the pinboard)',
                delete_after=8)
            return
        pinboard_channel = next((c for c in message.guild.channels if c.name == pinboard_name), None)
        if not pinboard_channel:
            await message.channel.send(
                f'Could not find pinboard channel #{pinboard_name}',
                delete_after=8)
            return
        wh_info_found = None
        for wh_info in await pinboard_channel.webhooks():
            if wh_info.token is not None:
                wh_info_found = wh_info
                break
        if wh_info_found is None:
            # Try to make a new webhook for the pinboard channel.
            wh_info_found = await pinboard_channel.create_webhook(name="cookiedough")
            if wh_info_found is None:
                await message.channel.send(
                    f'Failed to create webhook for pinboard channel #{pinboard_name}',
                    delete_after=8)
                return
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(wh_info_found.url, session=session)
            if webhook is None:
                log.error(f'Unable find a webhook in the #{pinboard_name} channel!')
                await message.channel.send(f'Unable find a webhook in the #{pinboard_name} channel!', delete_after=8)
                return
            pins = await message.channel.pins()
            if len(pins) <= 0:
                await message.channel.send(
                    f'Could not find any pins in <#{message.channel.id}>',
                    delete_after=8)
                return
            if pins[0].author.color.value == 0x000000:
                embdcolor = 0xb9bbbe
            else:
                embdcolor = pins[0].author.color

            enbd = Embed(
                description=f'[Jump To Message!]({pins[0].jump_url})\n(By {pins[0].author.mention} in <#{pins[0].channel.id}>)',
                color=embdcolor)
            if len(pins[0].embeds) > 0:

                if pins[0].embeds[0].type == 'video':
                    enbd.set_image(url=f'{pins[0].embeds[0].thumbnail.url}')
                    enbd.add_field(name='This pin has a video! :movie_camera:',
                                   value=f'**{pins[0].embeds[0].title}**\n[Jump]({pins[0].jump_url}) to watch!',
                                   inline=False)

                elif pins[0].embeds[0].type == 'image':
                    enbd.set_image(url=f'{pins[0].embeds[0].thumbnail.url}')

                elif pins[0].embeds[0].type == 'gifv':
                    if pins[0].embeds[0].provider.name == 'Giphy':
                        enbd.set_image(url=f'{pins[0].embeds[0].url}')
                    else:
                        enbd.set_image(url=f'{pins[0].embeds[0].thumbnail.proxy_url}')
                    if pins[0].embeds[0].provider.name == 'Tenor':
                        enbd.add_field(name='This pin has a video! :movie_camera:',
                                       value=f'[Jump]({pins[0].jump_url}) to watch!',
                                       inline=False)

                elif pins[0].embeds[0].type == 'rich':
                    enbd.add_field(name='** **',
                                   value=f'[{pins[0].embeds[0].author.name}]({pins[0].embeds[0].author.url})\n{pins[0].embeds[0].description}',
                                   inline=False)
                    if pins[0].embeds[0].image:
                        enbd.set_image(url=pins[0].embeds[0].image.url)
                    elif pins[0].embeds[0].thumbnail:
                        enbd.set_image(url=pins[0].embeds[0].thumbnail.url)
                        enbd.add_field(name='This pin has a video! :movie_camera:',
                                       value=f'[Jump]({pins[0].jump_url}) to watch!',
                                       inline=False)
                else:
                    if pins[0].embeds[0].image:
                        enbd.set_image(url=pins[0].embeds[0].image.url)
                    elif pins[0].embeds[0].thumbnail:
                        enbd.set_image(url=pins[0].embeds[0].thumbnail.url)
                        enbd.add_field(name='This pin may have a video! :movie_camera:',
                                       value=f'[Jump]({pins[0].jump_url}) to watch!',
                                       inline=False)
                    enbd.add_field(name='** **',
                                   value=f'**{pins[0].embeds[0].title}**\n{pins[0].embeds[0].description}',
                                   inline=False)

            if len(pins[0].attachments) > 0:
                if pins[0].attachments[0].filename.endswith(('.png', '.jpg', '.gif', '.jpeg', '.webp')):
                    enbd.set_image(url=f'{pins[0].attachments[0].url}')

                elif pins[0].attachments[0].filename.endswith(('.mp4', '.webm', '.mov')):
                    enbd.set_image(
                        url=f'{pins[0].attachments[0].proxy_url}?format=jpeg&width={pins[0].attachments[0].width}&height={pins[0].attachments[0].height}')
                    enbd.add_field(name='This pin could have a video! :movie_camera:',
                                   value=f'[Jump]({pins[0].jump_url}) to watch!',
                                   inline=False)

                elif pins[0].attachments[0].filename.endswith('.mp3'):
                    enbd.add_field(name='This pin has a sound file! :musical_note:',
                                   value=f'**{pins[0].attachments[0].filename}**\n[Jump]({pins[0].jump_url}) to listen!',
                                   inline=False)

                else:
                    enbd.add_field(name=f'This pin has an unembeddable file! :dividers:',
                                   value=f'**{pins[0].attachments[0].filename}**\n[Jump]({pins[0].jump_url}) to see it!',
                                   inline=False)

            if len(pins[0].embeds) + len(pins[0].attachments) > 1:
                enbd.add_field(name='This Pin Has _**Multiple Files**_ :dividers:',
                               value=f'[Jump]({pins[0].jump_url}) to see all of them!',
                               inline=False)

            if len(pins[0].content) > 0:
                enbd.add_field(name='** **', value=f'{pins[0].content}')

            enbd.set_footer(text=f'pinned by {message.author}')

            await webhook.send(avatar_url=f'{pins[0].author.avatar.url}',
                               username=pins[0].author.display_name,
                               embed=enbd)
            if message.author.id == self.bot.user.id:
                await pins[0].unpin()
                log.info(f'moved the message from {message.channel} to pinboard')
                return
            else:
                keeppin = await message.channel.send('Do you want me to keep the message pinned in here? (yes/no)')

            def check(m):
                return m.channel == message.channel and m.author == message.author and m.content.lower() in ('yes', 'no')
            try:
                keeppin_reply = await self.bot.wait_for('message', timeout=60.0, check=check)
                if keeppin_reply.content.lower() == 'yes':
                    await keeppin.delete()
                    await keeppin_reply.delete()
                elif keeppin_reply.content.lower() == 'no':
                    await pins[0].unpin()
                    await keeppin.delete()
                    await keeppin_reply.delete()
            except asyncio.TimeoutError:
                await pins[0].unpin()
                await keeppin.delete()
            log.info(f'{message.author} pinned a message in #{message.channel}')


async def setup(bot):
    await bot.add_cog(Pinboard(bot))
