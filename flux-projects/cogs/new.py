import discord
from discord.ext import commands


class New(commands.Cog):

    def __init__(self, flux):
        self.flux = flux


    @commands.command(brief='Create a new project.', help='Creates a new project. The bot will message you questions to complete the required information.')
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    async def new(self, ctx):
        await ctx.message.delete()
        await ctx.send(f'{ctx.author.mention}, To create a new project, please answer the questions I send to you in a private message.', delete_after=10)



def setup(flux):
    flux.add_cog(New(flux))