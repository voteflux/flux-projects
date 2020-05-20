import discord
from discord.ext import commands
import asyncio


class Question(commands.Cog):

    def __init__(self, flux):
        self.flux = flux


def setup(flux):
    flux.add_cog(Question(flux))