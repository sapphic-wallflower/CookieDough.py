import logging
import discord
from discord.ext import commands

log = logging.getLogger("cogs.main")


class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f'Cookie Dough is logged in as {self.bot.user}')
        await self.bot.change_presence(activity=discord.Game(f"{self.bot.command_prefix}help"))
        log.info(f'Set {self.bot.user} status to \"Playing {self.bot.command_prefix}help\"')

    def get_command_info(self, ctx):
        """Get command and args information from context"""
        msg = f'{ctx.command}'

        if len(ctx.args) > 0:
            # Find index of the context object
            ctx_index = -1
            for i, arg in enumerate(ctx.args):
                # Should be one of the first two as it's either ctx, args or cog,ctx,args
                if i >= 2:
                    break

                # Found the context object
                if type(arg) is commands.context.Context:
                    ctx_index = i
                    break

            # Include args to the RIGHT of the context object, or all of them if not found
            actual_args = ctx.args[ctx_index + 1:]
            if len(actual_args) > 0:
                msg = msg + f' args={actual_args}'

        if len(ctx.kwargs) > 0:
            msg = msg + f' kwargs={ctx.kwargs}'

        return msg

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        """Logs all commands that completed successfully"""
        command_info = self.get_command_info(ctx)
        log.info(f'{ctx.author} used [{command_info}] in #{ctx.channel}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Log all command failures except command not found"""
        if ctx.command is not None:
            command_info = self.get_command_info(ctx)
            log.info(f'{ctx.author} attempted to use [{command_info}] but failed with {error} ')
            reply = await ctx.send(f'{type(error).__name__}: {error}')
            await reply.delete(delay=1)
            raise error

    @commands.command()
    async def ping(self, ctx):
        """Replies with pong and the latency"""
        await ctx.send(f':ping_pong: Pong!`{round(ctx.bot.latency * 1000)} ms`')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def reload(self, ctx, *args):
        """Reload extension(s)"""
        # Hardcode for Nat - no longer necessary
        # if not ctx.message.author.permissions_in(ctx.message.channel).administrator:
        #     if not ctx.message.author.id == 235482330335019008:
        #         await ctx.channel.send(f"That command is for grown-ups, silly!")
        #         return
        if len(args) == 0:
            args = list(self.bot.extensions.keys())

        reloaded = []
        failed = []

        for name in set(args):
            try:
                ctx.bot.reload_extension(name)
                reloaded.append(name)
            except Exception as e:
                log.exception(f'Failed to reload {name}', exc_info=e)
                failed.append(f'{name}')

        msg = ""

        if len(reloaded) > 0:
            msg = msg + f'Reloaded: {" ".join(reloaded)}\n'

        if len(failed) > 0:
            msg = msg + f'Failed: {" ".join(failed)}\n'

        await ctx.send(f'```{msg.strip()}```')


def setup(bot):
    bot.add_cog(Main(bot))
