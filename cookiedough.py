import logging
import sys
from discord.ext import commands
from os import walk

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S')

description = '''A cookie loving Discord bot'''
bot = commands.Bot(command_prefix='.', description=description, case_insensitive=True)

cogpath = "cogs"
testmode = False

filenames = next(walk(cogpath+"/"), (None, None, []))[2] # Walk the cogs directory
for _,v in enumerate(filenames):  #Enumerate directory for iter
  v = v[:-3]
  if v == "testing" and not testmode: continue;
  try:
    bot.load_extension(cogpath+"."+str(v))
  except:
    print("Error in cog "+str(v)+". Could not load extension.")
    pass

bot.run(sys.argv[1])
