import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get
import requests
import utility.config_manager as config


class Issue(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='Create a new issue for DigiPol', help='Create a new issue for the app. You will be prompted to answer some questions by the bot.')
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    @commands.has_role('App Issue Creator')
    async def issue(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(description='You\'re now creating a new issue for the app, here is what I need to know from you:', colour=discord.Colour.green())
        await ctx.author.send(embed=embed)

        questions = [['text', 'What is the title of your issue?', 256],
                    ['date', 'What is the start date of your issue?'],
                    ['date', 'What is the end date of your issue?'],
                    ['text', 'What is the question of your issue?', 256],
                    ['text', 'What is the description of your issue?', 256],
                    ['text', 'What is the name of the sponsoring organisation?', 256]]
        
        qhand = self.flux.get_cog('Question')
        ans = await qhand.question_handler(ctx.author, questions)

        # Last value of ans will be True if all questions were asked
        if len(ans) == 0 or ans[-1] != True:
            return

        # Form dictionary for API request
        issue = {
            "token": config.read(('Bot', 'issue_token')),
            "data": {"chamber": "Public",
                    "short_title": ans[0],
                    "start_date": str(ans[1]),
                    "end_date": str(ans[2]),
                    "question": ans[3],
                    "description": ans[4],
                    "sponsor": ans[5]}}
        
        # Make the API POST request
        resp = requests.post('https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/issue', json=issue)

        # Raise an error if we don't get an OK response
        if resp.status_code != 201:
            raise commands.CommandError(f'POST /dev/issue {resp.status_code}')

        embed = discord.Embed(description='You have successfully created a new issue for the app.', colour=discord.Colour.green())
        await ctx.author.send(embed=embed)


def setup(flux):
    flux.add_cog(Issue(flux))