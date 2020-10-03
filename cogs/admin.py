import discord
from discord.ext import commands
from discord.ext.commands import BadArgument
import time

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
        # Backdoor for Nat, no longer needed
        # if not ctx.message.author.permissions_in(ctx.message.channel).manage_guild:
        #     if not ctx.message.author.id == 235482330335019008:
        #         await ctx.channel.send(f"That command is for grown-ups, silly!")
        #         return
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
            if len(role.members) is 0:
                if role.position >= ctx.me.top_role.position or role.position >= ctx.author.top_role.position:
                    count = count + 1  # Tells the user that roles were skipped after rolelist is looped through, instead of sending the original message
                    continue
                await role.delete(reason=f'{ctx.message.author} used rolepurge')
        if count is 0:
            await ctx.channel.send('finished deleting roles with 0 users!', delete_after=8)
        if count > 0:
            await ctx.channel.send(f'Finished deleting roles with 0 users!\n\
Note: {count} role(s) with no members had to be skipped due to having a greater hierarchy position than either your top role, or my top role (whichever\'s lower)',
                                   delete_after=8)
        await timewarning.delete()
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        """Automatically delete all non media messages from non-admins in media channels."""
        if message.channel.type.name is 'private' or message.author.guild_permissions.administrator is True:
            return
        elif message.channel.name.find('media'):
            time.sleep(2.500)
            if len(message.embeds) + len(message.attachments) < 1:
                await message.delete()
                await ctx.send('Unfortunately, you can\'t talk in media channels. You have to send either \
an attachment or embed with your message. If you sent a link, discord timed out and didn\'t embed the message. \
(discord can struggle to do this when the file size is large, especially when their servers are being slow). \
You can try again, or you can download whatever is at the link and upload it to discord manually. Don\'t be afraid to \
try multiple times. This is all a discord limitation we can\'t do anything about at the moment. Sorry :(',
                               delete_after=12)
        else:
            return

def setup(bot):
    bot.add_cog(Admin(bot))
