import discord
from discord.ext import commands


class Edit(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='Edit an existing project.', help='Edits an existing project. The bot will message you questions to complete the required information.')
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    async def edit(self, id):
        pass

def setup(flux):
    flux.add_cog(Edit(flux))