import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get
import utility.config_manager as config
from utility.db_manager import db_connection


class New(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='Create a new project.', help='Creates a new project. The bot will ask you to complete the required information.')
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    @commands.guild_only()
    async def new(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(description='You\'re now creating a new project, please complete the following information:', colour=discord.Colour.green())
        await ctx.author.send(embed=embed)

        fields = [['text', 'Title', 128],
                     ['date', 'Start date'],
                     ['date', 'End date'],
                     ['text', 'Description', 512],
                     ['text', 'Outcomes', 256],
                     ['text', 'Deliverables', 256],
                     ['choice', 'Objective', [
                         ['1️⃣', config.read(('Objectives', '1'))[0]],
                         ['2️⃣', config.read(('Objectives', '2'))[0]],
                         ['3️⃣', config.read(('Objectives', '3'))[0]],
                         ['4️⃣', config.read(('Objectives', '4'))[0]],
                         ['5️⃣', config.read(('Objectives', '5'))[0]],
                         ['6️⃣', config.read(('Objectives', '6'))[0]],
                         ['7️⃣', config.read(('Objectives', '7'))[0]],
                         ['8️⃣', config.read(('Objectives', '8'))[0]]], 
                         1],
                     ['choice', 'Resources', [
                         ['1️⃣', config.read(('Resources', '1'))[0]],
                         ['2️⃣', config.read(('Resources', '2'))[0]],
                         ['3️⃣', config.read(('Resources', '3'))[0]],
                         ['4️⃣', config.read(('Resources', '4'))[0]],
                         ['5️⃣', config.read(('Resources', '5'))[0]],
                         ['6️⃣', config.read(('Resources', '6'))[0]]],
                         6],
                     ['choice', 'Status', [
                         ['1️⃣', config.read(('Status', '1'))],
                         ['2️⃣', config.read(('Status', '2'))],
                         ['3️⃣', config.read(('Status', '3'))],
                         ['4️⃣', config.read(('Status', '4'))],
                         ['5️⃣', config.read(('Status', '5'))]],
                         1]]

        # Is this person verified to create official projects?
        role = get(ctx.guild.roles, name='Flux Vetted')
        
        if role in ctx.author.roles:
            fields.append(['choice', 'Officiality', [
                ['✅', 'Official'],
                ['❌', 'Not official']],
                1])
        
        field_handler = self.flux.get_cog('Field')
        ans = await field_handler.field_handler(ctx.author, fields)
        
        # Last value of ans will be True if all fields were complete
        if len(ans) == 0 or ans[-1] != True:
            return

        # Process resources list into string of key values
        resources = ''

        for i in ans[7]:
            resources += config.find_key_from_value('Resources', i)

        # Official is default 'No' unless the user was prompted
        if fields[-1][1] == 'Officiality':
            official = ans[9]
        else:
            official = 'No'

        # Process all data into a dict for clarity in SQL query and formatting as not every data point is asked for from the user
        ansdict = {
            "title": ans[0],
            "start_date": ans[1],
            "end_date": ans[2],
            "description": ans[3],
            "outcomes": ans[4],
            "deliverables": ans[5],
            "objective": config.find_key_from_value('Objectives', ans[6][0]),
            "lead": ctx.author.id,
            "resources": resources,
            "official": f"{1 if official == 'Official' else 0}",
            "status": config.find_key_from_value('Status', ans[8][0])
        }

        # Insert the new project
        with db_connection() as db:
            db.execute(f"INSERT INTO `projects` (title, start_date, end_date, description, outcomes, deliverables, objective, lead, resources, official, status) VALUES ('{ansdict['title']}', '{ansdict['start_date']}', '{ansdict['end_date']}', '{ansdict['description']}', '{ansdict['outcomes']}', '{ansdict['deliverables']}', {ansdict['objective']}, {ansdict['lead']}, '{ansdict['resources']}', {ansdict['official']}, {ansdict['status']})")

        pinfo = self.flux.get_cog('Info')
        embed = discord.Embed(description=f'You have successfully created a new project with the ID `{await pinfo.get_latest_project_ID()}`', colour=discord.Colour.green())
        await ctx.author.send(embed=embed)


def setup(flux):
    flux.add_cog(New(flux))
