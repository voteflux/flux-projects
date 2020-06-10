import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get


class Issue(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='Create a new issue for DigiPol', help='Create a new issue for the app. You will be prompted to answer some questions by the bot.')
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    @commands.has_role('Flux Vetted')
    async def issue(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(description='You\'re now creating a new issue for the app, here is what I need to know from you:', colour=discord.Colour.green())
        await ctx.author.send(embed=embed)

        questions = [['text', 'What is the title if your issue?', 64],
                    ['date', 'What is the start date of your issue?'],
                    ['date', 'What is the end date of your issue?'],
                    ['text', 'What is the question of your issue?', 128],
                    ['text', 'What is the description of your issue?', 256],
                    ['text', 'What is the name of the sponsoring organisation?', 64]]
        
        qhand = self.flux.get_cog('Question')
        ans = await qhand.question_handler(ctx.author, questions)


def setup(flux):
    flux.add_cog(Issue(flux))