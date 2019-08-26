import logging

from discord.ext import commands

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


def setup(bot):
    bot.add_cog(Testing(bot))
