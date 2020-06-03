import discord
from discord.ext import commands
import asyncio
from datetime import datetime


class Question(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    async def question_handler(self, user: discord.User, questions: list):
        answers = []
        for q in questions:
            if q[0] == 'text':
                answers.append(await self.question_text(user, q[1], q[2]))
            elif q[0] == 'date':
                answers.append(await self.question_date(user, q[1]))
            elif q[0] == 'choice':
                answers.append(await self.question_choice(user, q[1], q[2], q[3]))
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

        answer = await self.await_reply(user)
        if answer == None:
            return

        try:
            date = datetime.strptime(answer.content, '%Y-%m-%d').date()

        except ValueError:
            embed = discord.Embed(description=f'You must answer a valid date in the format YYYY-MM-DD.', colour=discord.Colour.red())
            await user.send(embed=embed)
            return await self.question_date(user, question)

        else:
            return date

    async def question_choice(self, user: discord.User, question, choices, max_choices):
        approve_reaction = '➡️'

        # Form question embed
        embed = discord.Embed(title=question, description=f'React with your {"answers" if max_choices > 1 else "answer"} and then {approve_reaction} once you\'re finished.', colour=discord.Colour.green())
        embed.set_footer(text=f'You have up to {max_choices} {"answers" if max_choices > 1 else "answer"}.')
        
        for q in choices:
            embed.add_field(name='\u200b', value=f'{q[0]} {q[1]}', inline=False)
        
        # Send question embed, message known as qmsg
        qmsg = await user.send(embed=embed)

        # Add a reaction for each possible answer
        for e in choices:
            await qmsg.add_reaction(e[0])

        # Add reaction to finalise selection
        # We listen for this reaction and return a list of all reactions to qmsg upon this
        await qmsg.add_reaction(approve_reaction)

        reactions = await self.await_react(user, qmsg, approve_reaction)

        # Forward the reactions list to a processing function self.process_choices
        # This is where the returned reaction data is interrpeted and all necessary checks occur
        return await self.process_choices(user, question, choices, max_choices, reactions)

    async def process_choices(self, user: discord.User, question, choices, max_choices, reactions):
        answers = []

        for i, r in enumerate(reactions):
            # A count over 1 is considered a selection
            # A user also can't add a new emoji more than once in a PM, so there is no need to filter for that
            if r.count > 1:
                answers.append(i)

        # Has the user made more selections than they're allowed?
        if len(answers) > max_choices:
            embed = discord.Embed(description=f'You are only allowed up to {max_choices} {"answers" if max_choices > 1 else "answer"}.', colour=discord.Colour.red())
            await user.send(embed=embed)
            return await self.question_choice(user, question, choices, max_choices)

        return answers

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

    async def await_react(self, user: discord.User, msg: discord.Message, approve_reaction: str):
        def check(reaction, reactor):
            return reactor == user and str(reaction.emoji) == approve_reaction
        
        try:
            reaction, reactor = await self.flux.wait_for('reaction_add', timeout=60, check=check)
        
        except asyncio.TimeoutError as e:
            embed = discord.Embed(description='You did not answer the question in time.', colour=discord.Colour.red())
            await user.send(embed=embed)
            return
        
        else:
            rmsg = await user.fetch_message(msg.id)
            rmsg.reactions.pop()
            return rmsg.reactions

def setup(flux):
    flux.add_cog(Question(flux))