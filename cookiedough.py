import logging
import sys

from discord.ext import commands

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d_%H:%M:%S')

description = '''A cookie loving Discord bot'''
bot = commands.Bot(command_prefix='.', description=description)

bot.load_extension("cogs.main")

bot.run(sys.argv[1])
