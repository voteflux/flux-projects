import discord
from discord.ext import commands
import asyncio


class Question(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    async def question_handler(self, user: discord.User, questions: tuple):
        answers = []
        for q in questions:
            if q[0] == 'text':
                answers.append(await self.question_text(user, q[1]))

    async def question_text(self, user: discord.User, question):
        embed = discord.Embed(description=question, colour=discord.Colour.green())
        await user.send(embed=embed)
        def check(m):
            return m.author == user and isinstance(m.channel, discord.DMChannel)
        
        try:
            answer = await self.flux.wait_for('message', timeout=60, check=check)

        except asyncio.TimeoutError as e:
            embed = discord.Embed(description='You did not answer the question in time.', colour=discord.Colour.red())
            await user.send(embed=embed)
            return

        else:
            return answer.content

def setup(flux):
    flux.add_cog(Question(flux))