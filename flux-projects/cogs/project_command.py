import discord
from discord.ext import commands
import mysql.connector
import config_manager as config


class Project_Command(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.group()
    async def project(self, ctx):
        pass

    @project.command(brief='View information about a specific project.', help='View all information about the specified project.')
    async def view(self, ctx, id: int = None):
        content = ""

        if id is None:
            id = await self.get_latest_project_ID()
            content = "This is the latest project:"

        try:
            db = mysql.connector.connect(**config.db_config())

            if db.is_connected:
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM `projects` WHERE `id` = \'{id}\' LIMIT 1')

        except mysql.connector.Error as e:
            raise e

        else:
            project = cursor.fetchone()

            author = ctx.guild.get_member(project[8])

            # API request for a User object instead of a Member object incase the user is no longer in the guild
            if author is None:
                author = await self.flux.fetch_user(project[8])
            
            cursor.close()
            db.close()

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
        
        try:
            db = mysql.connector.connect(**config.db_config())

            if db.is_connected:
                cursor = db.cursor()
                cursor.execute('SELECT id FROM `projects` ORDER BY `projects`.`id` DESC LIMIT 1')

        except mysql.connector.Error as e:
            raise e

        else:
            project_ID = cursor.fetchone()
            
            cursor.close()
            db.close()

            return project_ID[0]


def setup(flux):
    flux.add_cog(Project_Command(flux))