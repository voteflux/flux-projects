import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get
import utility.config_manager as config


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
                     ['choice', 'What is the objective of your project?', [
                         ['1️⃣', config.read(('Objectives', '1'))[0]],
                         ['2️⃣', config.read(('Objectives', '2'))[0]],
                         ['3️⃣', config.read(('Objectives', '3'))[0]],
                         ['4️⃣', config.read(('Objectives', '4'))[0]],
                         ['5️⃣', config.read(('Objectives', '5'))[0]],
                         ['6️⃣', config.read(('Objectives', '6'))[0]],
                         ['7️⃣', config.read(('Objectives', '7'))[0]],
                         ['8️⃣', config.read(('Objectives', '8'))[0]]], 
                         1],
                     ['choice', 'What resources does your project require?', [
                         ['1️⃣', config.read(('Resources', '1'))[0]],
                         ['2️⃣', config.read(('Resources', '2'))[0]],
                         ['3️⃣', config.read(('Resources', '3'))[0]],
                         ['4️⃣', config.read(('Resources', '4'))[0]],
                         ['5️⃣', config.read(('Resources', '5'))[0]],
                         ['6️⃣', config.read(('Resources', '6'))[0]]],
                         6],
                     ['choice', 'What is the status of your project?', [
                         ['1️⃣', config.read(('Status', '1'))],
                         ['2️⃣', config.read(('Status', '2'))],
                         ['3️⃣', config.read(('Status', '3'))],
                         ['4️⃣', config.read(('Status', '4'))],
                         ['5️⃣', config.read(('Status', '5'))]],
                         1]]

        # Should this person be able to create official projects?
        role = get(ctx.guild.roles, name='Flux Vetted')
        
        if role in ctx.author.roles:
            questions.append(['choice', 'Is this an official Flux project?', [
                ['✅', 'Yes'],
                ['❌', 'No']],
                1])
        else:
            official = False
        
        answers = await self.question.question_handler(ctx.author, questions)
        await ctx.send(answers)


def setup(flux):
    flux.add_cog(New(flux))