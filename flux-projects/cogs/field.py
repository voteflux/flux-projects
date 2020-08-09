import discord
from discord.ext import commands
import asyncio
from datetime import datetime


class Field(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    async def field_handler(self, user: discord.User, fields):
        answers = []
        for f in fields:
            
            if f[0] == 'text':
                ans = await self.text_field(user, f[1], f[2])
                if ans == None:
                    return answers
                answers.append(ans)

            elif f[0] == 'date':
                ans = await self.date_field(user, f[1])
                if ans == None:
                    return answers
                answers.append(ans)

            elif f[0] == 'choice':
                ans = await self.choice_field(user, f[1], f[2], f[3])
                if ans == None:
                    return answers
                answers.append(ans)
        
        answers.append(True)
        return answers

    async def text_field(self, user: discord.User, field, char_limit: 0):
        embed = discord.Embed(title=field, colour=discord.Colour.green())
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
            return await self.text_field(user, field, char_limit)

    async def date_field(self, user: discord.User, field):
        embed = discord.Embed(title=field, colour=discord.Colour.green())
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
            return await self.date_field(user, field)

        else:
            return date

    async def choice_field(self, user: discord.User, field, choices, max_choices):
        approve_reaction = '➡️'

        # Form field embed
        embed = discord.Embed(title=field, description=f'React with your {"answers" if max_choices > 1 else "answer"} and then {approve_reaction} once you\'re finished.', colour=discord.Colour.green())
        embed.set_footer(text=f'You have up to {max_choices} {"answers" if max_choices > 1 else "answer"}.')
        
        for c in choices:
            embed.add_field(name='\u200b', value=f'{c[0]} {c[1]}', inline=False)
        
        # Send field embed, message known as fmsg
        fmsg = await user.send(embed=embed)

        # Add a reaction for each possible answer
        for e in choices:
            await fmsg.add_reaction(e[0])

        # Add reaction to finalise selection
        # We listen for this reaction and return a list of all reactions to fmsg upon this
        await fmsg.add_reaction(approve_reaction)

        reactions = await self.await_react(user, fmsg, approve_reaction)
        if reactions == None:
            return

        # Forward the reactions list to a processing function self.process_choices
        # This is where the returned reaction data is interrpeted and all necessary checks occur
        return await self.process_choices(user, field, choices, max_choices, reactions)

    async def process_choices(self, user: discord.User, field, choices, max_choices, reactions):
        answers = []

        for i, r in enumerate(reactions):
            # A count over 1 is considered a selection
            # A user also can't add a new emoji more than once in a PM, so there is no need to filter for that
            if r.count > 1:
                answers.append(choices[i][1])

        # Has the user made more selections than they're allowed?
        if len(answers) > max_choices:
            embed = discord.Embed(description=f'You are only allowed up to {max_choices} {"answers" if max_choices > 1 else "answer"}.', colour=discord.Colour.red())
            await user.send(embed=embed)
            return await self.choice_field(user, field, choices, max_choices)

        return answers

    async def await_reply(self, user: discord.User):
        def check(m):
            return m.author == user and isinstance(m.channel, discord.DMChannel)
        
        try:
            answer = await self.flux.wait_for('message', timeout=60, check=check)

        except asyncio.TimeoutError as e:
            embed = discord.Embed(description='You did not complete the field in time.', colour=discord.Colour.red())
            await user.send(embed=embed)
            return

        else:
            return answer

    async def await_react(self, user: discord.User, msg, approve_reaction):
        def check(reaction, reactor):
            return reactor == user and str(reaction.emoji) == approve_reaction
        
        try:
            reaction, reactor = await self.flux.wait_for('reaction_add', timeout=60, check=check)
        
        except asyncio.TimeoutError as e:
            embed = discord.Embed(description='You did not complete the field in time.', colour=discord.Colour.red())
            await user.send(embed=embed)
            return
        
        else:
            rmsg = await user.fetch_message(msg.id)
            rmsg.reactions.pop()
            return rmsg.reactions

def setup(flux):
    flux.add_cog(Field(flux))