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
                answers.append(await self.question_text(user, q[1], q[2]))
        return answers

    async def question_text(self, user: discord.User, question, char_limit: int = 0):
        embed = discord.Embed(title=question, colour=discord.Colour.green())
        embed.set_footer(text=f'Character limit: {char_limit if char_limit > 0 else "No limit"}')
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
            if len(answer.content) <= char_limit or char_limit == 0:
                return answer.content
            else:
                embed = discord.Embed(description=f'You must answer in {char_limit} characters or less.', colour=discord.Colour.red())
                await user.send(embed=embed)
                await self.question_text(user, question, char_limit) 


def setup(flux):
    flux.add_cog(Question(flux))