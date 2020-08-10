import discord
from discord.ext import commands
from utility.db_manager import db_connection
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get
import utility.config_manager as config


class Edit(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='Edit an existing project.', help='Edits an existing project. The bot will ask you to complete the required information.')
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    @commands.guild_only()
    async def edit(self, ctx, id):
        await ctx.message.delete()

        # Get the specified project
        with db_connection() as db:
            db.execute(f'SELECT * FROM `projects` WHERE `id` = \'{id}\' LIMIT 1')
            project = db.fetchone()

        # Is this person the project owner or are they authorised to edit any project?
        bot_admin = get(ctx.author.roles, name='Flux Vetted')

        if bot_admin or project[8] == ctx.author.id:
            pass
        
        else:
            embed = discord.Embed(description=f'Only the project owner or Bot Admin can edit this project.', colour=discord.Colour.red())
            return await ctx.author.send(embed=embed)
            

        embed = discord.Embed(description=f'You\'re now editing project `{id}`, please review the existing information and update each field:', colour=discord.Colour.green())
        await ctx.author.send(embed=embed)

        # Send existing project info
        info_cog = self.flux.get_cog('Info')
        data = await info_cog.form_project_data(ctx, project, 'longer')
        await ctx.author.send(embed=data)
        
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

        if bot_admin:
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

        # Update the existing project
        with db_connection() as db:
            db.execute(f"UPDATE `projects` SET title = '{ansdict['title']}', start_date = '{ansdict['start_date']}', end_date = '{ansdict['end_date']}', description = '{ansdict['description']}', outcomes = '{ansdict['outcomes']}', deliverables = '{ansdict['deliverables']}', objective = {ansdict['objective']}, lead = {ansdict['lead']}, resources = '{ansdict['resources']}', official = {ansdict['official']}, status = {ansdict['status']} WHERE id = {id}")

        embed = discord.Embed(description=f'You have successfully edited the existing project `{id}`', colour=discord.Colour.green())
        await ctx.author.send(embed=embed)

def setup(flux):
    flux.add_cog(Edit(flux))