import discord
from discord.ext import commands


class Ping(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='Check the bot\'s latency.', help='Check the bot\'s latency or whether it\'s responding at all.')
    async def ping(self, ctx):
        await ctx.send(f'Pong! That took me {round(self.flux.latency * 1000)}ms!')


def setup(flux):
    flux.add_cog(Ping(flux))