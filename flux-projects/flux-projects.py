import discord
from discord.ext import commands

flux = commands.Bot(command_prefix='!', case_insensitive=True)


@flux.event
async def on_ready():
    print('Flux Projects bot is ready.')


flux.run('token')
