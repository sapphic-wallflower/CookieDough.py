import logging
import sys

from discord.ext import commands

logging.basicConfig(level=logging.INFO, format='%(message)s %(asctime)s', datefmt='%m/%d/%Y %I:%M:%S %p')

description = '''A cookie loving Discord bot'''
bot = commands.Bot(command_prefix='.', description=description)


@bot.event
async def on_ready():
    print(f'Cookie Dough is logged in as {bot.user}')


@bot.event
async def on_command_completion(ctx):
    """Logs all commands that completed without error"""
    logging.info(f'{ctx.author} used {ctx.command} with args={ctx.args} and kwargs={ctx.kwargs}')


@bot.command()
async def ping(ctx):
    """Replies with pong and the latency"""
    await ctx.send(f":ping_pong: Pong! `{round(bot.latency * 1000)} ms`")


bot.run(sys.argv[1])
