import logging
import sys

from discord.ext import commands

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d_%H:%M:%S')

description = '''A cookie loving Discord bot'''
bot = commands.Bot(command_prefix='.', description=description)


@bot.event
async def on_ready():
    logging.info(f'Cookie Dough is logged in as {bot.user}')


@bot.event
async def on_command_completion(ctx):
    """Logs all commands that completed successfully"""
    msg = f'{ctx.author} used {ctx.command}'
    if len(ctx.args) > 1:
        msg = msg + f' args={ctx.args[1:]}'
    if len(ctx.kwargs) > 0:
        msg = msg + f' kwargs={ctx.kwargs}'
    logging.info(msg)


@bot.command()
async def ping(ctx):
    """Replies with pong and the latency"""
    await ctx.send(f":ping_pong: Pong! `{round(bot.latency * 1000)} ms`")


bot.run(sys.argv[1])
