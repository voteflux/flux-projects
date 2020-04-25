import discord
from discord.ext import commands
import utility.config_manager as config
from discord.ext.commands.cooldowns import BucketType
from utility.db_manager import db_connection


class Info(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='View information about a specific project.', help='View all information about the specified project or the latest project to be created if no project ID is is specified.')
    async def info(self, ctx, id: int = None):
        content = ""

        if id is None:
            id = await self.get_latest_project_ID()
            content = "This is the latest project:"

        with db_connection() as db:
            db.execute(f'SELECT * FROM `projects` WHERE `id` = \'{id}\' LIMIT 1')
            project = db.fetchone()

        if project is None:
            await ctx.message.delete()
            return await ctx.send(f'{ctx.author.mention}, There are no projects by the ID `{id}`.', delete_after=10)

        author = ctx.guild.get_member(project[8])

        # API request for a User object instead of a Member object incase the user is no longer in the guild
        if author is None:
            author = await self.flux.fetch_user(project[8])

        colour = await commands.ColourConverter.convert(self, ctx, config.objective_data(str(project[7]))[1])

        embed = discord.Embed(title=project[1], description=project[4], color=colour)
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        
        # Unnecessary information. Can be used later on for in depth message about project.
        
        # This field is a blank line break for inline field organising purposes
        #embed.add_field(name='\u200b', value='\u200b', inline=False)
        #embed.add_field(name='Resouces', value=project[9], inline=True)
        #embed.add_field(name='Outcomes', value=project[5], inline=True)
        #embed.add_field(name='Deliverables', value=project[6], inline=True)
        embed.add_field(name='Objective', value=config.objective_data(str(project[7]))[0], inline=True)
        embed.add_field(name='Completion', value=project[3], inline=True)
        embed.add_field(name='Status', value=project[11], inline=True)
        embed.set_footer(text=f'Project ID #{project[0]}  |  Flux {"Official" if project[10] else "Volunteer"} Project')

        await ctx.send(content=content, embed=embed)

    async def get_latest_project_ID(self):
        with db_connection() as db:
            db.execute('SELECT id FROM `projects` ORDER BY `projects`.`id` DESC LIMIT 1')
            project_ID = db.fetchone()
            return project_ID[0]
'''
    @commands.command(brief='Create a new project.', help='Creates a new project. The bot will message you questions to complete the required information.')
    @commands.max_concurrency(1, per=BucketType.user, wait=False)
    async def new(self, ctx):
        await ctx.message.delete()
        await ctx.send(f'{ctx.author.mention}, To create a new project, please answer the questions I send to you in a private message.', delete_after=10)
'''

def setup(flux):
    flux.add_cog(Info(flux))