import discord
from discord.ext import commands
import config_manager as config
import os

print(config.check())

flux = commands.Bot(command_prefix=config.read('bot_prefix'), case_insensitive=True)


@flux.event
async def on_ready():
    print('Flux Projects bot is ready.')

# Loading of all cog files in the cogs directory
for filename in os.listdir('flux-projects/cogs'):
    if filename.endswith('.py'):
        flux.load_extension(f'cogs.{filename[:-3]}')


flux.run(config.read('bot_token'))
