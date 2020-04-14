import discord
from discord.ext import commands
import mysql.connector
import config_manager as config


class Project_Info(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='View information about a specific project.', help='View all information about the specified project.')
    async def project(self, ctx, id=None):
        if id is None:
            id = await self.get_latest_project_ID()

        try:
            db = mysql.connector.connect(**config.db_config())

            if db.is_connected:
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM `projects` WHERE `id` = \'{id}\' LIMIT 1')

        except mysql.connector.Error as e:
            raise e

        else:
            project = cursor.fetchone()
            
            cursor.close()
            db.close()

            await ctx.send(f'{project}')

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
    flux.add_cog(Project_Info(flux))