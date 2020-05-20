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
            elif q[0] == 'date':
                answers.append(await self.question_date(user, q[1]))
        return answers

    async def question_text(self, user: discord.User, question, char_limit: int = 0):
        embed = discord.Embed(title=question, colour=discord.Colour.green())
        embed.set_footer(text=f'Character limit: {char_limit if char_limit > 0 else "No limit"}')
        await user.send(embed=embed)

        answer = await self.await_reply(user)
        if answer == None:
            return

        if len(answer.content) <= char_limit or char_limit == 0:
            return answer.content
        else:
            embed = discord.Embed(description=f'You must answer in {char_limit} characters or less.', colour=discord.Colour.red())
            await user.send(embed=embed)
            return await self.question_text(user, question, char_limit)

    async def question_date(self, user: discord.User, question):
        embed = discord.Embed(title=question, colour=discord.Colour.green())
        embed.set_footer(text='Use the format YYYY-MM-DD')
        await user.send(embed=embed)

    async def await_reply(self, user: discord.User):
        def check(m):
            return m.author == user and isinstance(m.channel, discord.DMChannel)
        
        try:
            answer = await self.flux.wait_for('message', timeout=60, check=check)

        except asyncio.TimeoutError as e:
            embed = discord.Embed(description='You did not answer the question in time.', colour=discord.Colour.red())
            await user.send(embed=embed)
            return

        else:
            return answer


def setup(flux):
    flux.add_cog(Question(flux))