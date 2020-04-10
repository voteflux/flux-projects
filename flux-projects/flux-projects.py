import discord
from discord.ext import commands
import config_manager as config

print(config.check())

flux = commands.Bot(command_prefix=config.read('bot_prefix'), case_insensitive=True)


@flux.event
async def on_ready():
    print('Flux Projects bot is ready.')


flux.run(config.read('bot_token'))
