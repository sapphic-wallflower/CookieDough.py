import asyncio
import discord
from discord import MessageType, ChannelType
from discord.ext import commands
from discord.ext.commands import BadArgument


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx: commands.context.Context, n: int):
        """Purge `n` messages"""
        if n <= 0 or n > 49:
            raise BadArgument("n should be in [1,49]")
        deleted = await ctx.channel.purge(limit=n + 1)
        reply = await ctx.send(f'{len(deleted) - 1} message(s) purged')
        await reply.delete(delay=1)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def status(self, ctx):
        """Set the bot's playing status"""
        command_prefix = self.bot.command_prefix
        if ctx.message.system_content == f'{command_prefix}status clear':
            await self.bot.change_presence(activity=discord.Game(f"{command_prefix}help"))
            await ctx.channel.send(f"Set status to \"Playing **{command_prefix}help**\"!")
        else:
            message = ctx.message.system_content.replace(f'{command_prefix}status ', '')
            await self.bot.change_presence(activity=discord.Game(f"{command_prefix}help | {message}"))
            await ctx.channel.send(f"Set status to \"Playing **{command_prefix}help | {message}**\"!")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def say(self, ctx):
        """Have Cookie Dough repeat a phrase in a channel"""
        # perhaps we ought to add functionality where the channel can be unspecified and cookie defaults to the ctx.channel?
        # needs check or exception for editing a message in another channel
        command_prefix = self.bot.command_prefix
        target_channel_id = ctx.message.raw_channel_mentions[0]
        if ctx.message.content.startswith(f'{command_prefix}say <#{target_channel_id}> ') is False:
            await ctx.channel.send(
                f"use `{command_prefix}say [target_channel] [message]` to have me say the contents of [message] in whatever channel you pick!")
            return
        msg = ctx.message.content.replace(f'{command_prefix}say <#{target_channel_id}> ', '')
        for channel in ctx.message.guild.channels:
            if channel.id == target_channel_id:
                await channel.send(f"{msg}")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def edit(self, ctx, *args):
        """Have Cookie Dough replace the contents of a message she sent using .say"""
        #perhaps we ought to add the ability to "s/e/x" hack edit messages ".edit [id] tyop/typo" for instance?
        command_prefix = self.bot.command_prefix
        target_message = await ctx.fetch_message(args[0])
        if ctx.message.content.startswith(f'{command_prefix}edit {target_message.id}') is False:
            await ctx.channel.send(
                f"use `{command_prefix}say [target_message_raw_id] [new contents]` to have me edit the contents of the targeted message with new contents!")
            return
        if target_message.author.id != self.bot.user.id:
            await ctx.channel.send(
                f"I can only edit my own messages! I wouldn't want to put words in someone else's mouth... What if they sue!? <:MeruImpureThoughts:633650580824391693>")
            return
        content = ctx.message.content.replace(f'{command_prefix}edit {target_message.id} ', '')
        await target_message.edit(content=f"{content}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def pinpurge(self, ctx, n: int):
        """Delete all pins in a channel, except ones sent from cookiedough"""
        command_prefix = self.bot.command_prefix
        pins = await ctx.message.channel.pins()
        count = 0
        if n <= 0 or n > 50 or n is None:
            await ctx.channel.send(
                f'how many pins did you want me to unpin in this channel? (`{command_prefix}pinpurge [number]`(min 1, max 50))')
            return
        timewarning = await ctx.channel.send(f'unpinning {n} pins in this channel, this may take awhile...')
        for pin in pins:
            if pin.author.id == ctx.me.id:
                continue
            if count > n:
                break
            await pin.unpin()
            count = count + 1
        await ctx.channel.send('finished unpinning!', delete_after=8)
        await timewarning.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def rolepurge(self, ctx):
        """Delete all roles in the server that have 0 users"""
        rolelist = ctx.guild.roles
        timewarning = await ctx.channel.send('Deleting roles with 0 users, this may take awhile...')
        count = 0
        for role in rolelist:
            if len(role.members) == 0:
                if role.position >= ctx.me.top_role.position or role.position >= ctx.author.top_role.position:
                    count = count + 1  # Tells the user that roles were skipped after rolelist is looped through, instead of sending the original message
                    continue
                await role.delete(reason=f'{ctx.message.author} used rolepurge')
        if count == 0:
            await ctx.channel.send('finished deleting roles with 0 users!', delete_after=8)
        if count > 0:
            await ctx.channel.send(f'Finished deleting roles with 0 users!\n\
Note: {count} role(s) with no members had to be skipped due to having a greater hierarchy position than either your top role, or my top role (whichever\'s lower)',
                                   delete_after=8)
        await timewarning.delete()
        await ctx.message.delete()


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message): # known bug: wont act as media channel if channel contains text 'original' or 'selfies'
        """Automatically delete non-media messages in media channels | add 📌 and/or 🍪 reaction to media messages"""
        if message.channel.name.find('original') > -1 or message.channel.name.find('selfies') > -1:  # looks for the position of substring. if it's not found, this returns -1.
            await asyncio.sleep(2.500) #wait for embeds
            if len(message.embeds) + len(message.attachments) > 0:
                await message.add_reaction('📌')
                await message.add_reaction('<:CookieHeart:673558008185487381>')
                return
        
        if message.author.id == self.bot.user.id:
            return
        # We need to check if it is a member in addition since webhook message authors are not members and can't have permissions.
        if message.author is discord.Member and message.author.guild_permissions.administrator:
            return
        if message.channel.type != ChannelType.text:
            return
        if message.type not in (MessageType.default, MessageType.reply):
            return
        if message.channel.name.find(
                'media') == -1:  # looks for the position of substring. if it's not found, this returns -1.
            return
        
        await asyncio.sleep(2.500) #wait for embeds
        if len(message.embeds) + len(message.attachments) > 0:
            await message.add_reaction('📌')  # doesn't check if channel is private, only if media isn't in the name
            return
        try:
            await message.channel.send(f'<@{message.author.id}> Sorry, you can\'t talk in media channels, but you can start a thread! if you posted media, try again and make sure it embedded properly',
                                       delete_after=8)
            await message.delete()
        except discord.NotFound: # Message was already deleted.
            pass

async def setup(bot):
    await bot.add_cog(Admin(bot))
