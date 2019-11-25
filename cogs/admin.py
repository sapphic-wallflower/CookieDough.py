import discord
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
        deleted = await ctx.channel.purge(limit=n+1)
        reply = await ctx.send(f'{len(deleted)-1} message(s) purged')
        await reply.delete(delay=1)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def status(self, bot):
        """Set the bot's playing status"""
        command_prefix = self.bot.command_prefix
        if bot.message.system_content == f'{command_prefix}status clear':
            await self.bot.change_presence(activity=discord.Game(f"{command_prefix}help"))
            await bot.channel.send(f"Set status to \"Playing **{command_prefix}help**\"!")
        else:
            message = bot.message.system_content.replace(f'{command_prefix}status ', '')
            await self.bot.change_presence(activity=discord.Game(f"{command_prefix}help | {message}"))
            await bot.channel.send(f"Set status to \"Playing **{command_prefix}help | {message}**\"!")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def say(self, bot):
        """Have Cookie Dough repeat a phrase in a channel"""
        command_prefix = self.bot.command_prefix
        target_channel_id = bot.message.raw_channel_mentions[0]
        if bot.message.content.startswith(f'{command_prefix}say <#{target_channel_id}> ') is False:
            await bot.channel.send(f"use `{command_prefix}say [target_channel] [message]` to have me say the contents of [message] in whatever channel you pick!")
            return
        msg = bot.message.content.replace(f'{command_prefix}say <#{target_channel_id}> ', '')
        for channel in bot.message.guild.channels:
            if channel.id == target_channel_id:
                await channel.send(f"{msg}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def pinpurge(self, bot, n: int):
        """Delete all pins in a channel, except ones sent from cookiedough"""
        command_prefix = self.bot.command_prefix
        pins = await bot.message.channel.pins()
        count = 0
        if n <= 0 or n > 49:
            await bot.channel.send(f'how many pins did you want me to unpin in this channel? (`{command_prefix}pinpurge [number]`)')
            return
        timewarning = await bot.channel.send(f'unpinning {n} pins in this channel, this may take awhile...')
        for pin in pins:
            if pin.author.id == bot.me.id:
                continue
            if count > n:
                break
            await pin.unpin()
            count = count+1
        await bot.channel.send('finished unpinning!', delete_after=8)
        await timewarning.delete()
        await bot.message.delete()


def setup(bot):
    bot.add_cog(Admin(bot))
