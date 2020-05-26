import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get


class New(commands.Cog):

    def __init__(self, flux):
        self.flux = flux
        self.question = self.flux.get_cog('Question')

    @commands.command(brief='Create a new project.', help='Creates a new project. The bot will message you questions to complete the required information.')
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    async def new(self, ctx):
        await ctx.message.delete()
        await ctx.send(f'{ctx.author.mention}, To create a new project, please answer the questions I send to you in a private message.', delete_after=10)

        questions = [['text', 'What is your project title?', 128],
                     ['date', 'What is the start date of your project?'],
                     ['date', 'What is the end date of your project?'],
                     ['text', 'What is the desciption of your project?', 512],
                     ['text', 'What are the outcomes of your project?', 256],
                     ['text', 'What are the deliverables of your project?', 256],
                     ['text', 'What is the objective of your project? *This is a placeholder for an unsupported question type.*', 100],
                     ['text', 'What resources does your project require? *This is a placeholder for an unsupported question type.*', 100],
                     ['text', 'What is the status of your project? *This is a placeholder for an unsupported question type.*', 100]]

        # Should this person be able to create official projects?
        role = get(ctx.guild.roles, name='Flux Vetted')
        
        if role in ctx.author.roles:
            questions.append(['text', 'Is this an official Flux project? *This is a placeholder for an unsupported question type.*', 100])
        else:
            official = False
        
        answers = await self.question.question_handler(ctx.author, questions)
        await ctx.send(answers)


def setup(flux):
    flux.add_cog(New(flux))