import discord
from discord.ext import commands
from utility.db_manager import db_connection
import utility.config_manager as config


class Filter(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='Returns all projects with the specified status.', help='View all projects with the specified status. You can specify how much detail to show by including a detail argument. Avaliable statuses: active, open, done, blocked, out of scope. Detail options: short, long, longer.')
    @commands.has_role('Server Admin')
    async def filter(self, ctx, status: str = 'active', detail: str = 'short'):
        # We don't want case to be a factor
        status = status.lower()
        detail = detail.lower()
        
        # Raise error if input is invalid
        valid_status = config.read_section_values('Status')
        valid_detail = ['short', 'long', 'longer']

        if status not in valid_status or detail not in valid_detail:
            raise commands.UserInputError
        
        status_id = config.find_key_from_value('Status', status)
        with db_connection() as db:
            db.execute(f'SELECT * FROM `projects` WHERE `status` = \'{status_id}\'')
            projects = db.fetchall()

        if len(projects) == 0:
            await ctx.message.delete()
            embed = discord.Embed(description=f'{ctx.author.mention}, There are no projects with the `{status.title()}` status.', colour=discord.Colour.red())
            await ctx.send(embed=embed, delete_after=10)
            return

        embed = discord.Embed(description=f'Here are all projects with the `{status.title()}` status:', colour=discord.Colour.green())
        embed.set_footer(text=f'Detail: {detail.title()}, Total: {len(projects)}')
        await ctx.send(embed=embed)
        
        info_cog = self.flux.get_cog('Info')
        for project in projects:
            data = await info_cog.form_project_data(ctx, project, detail)
            await ctx.send(embed=data)


def setup(flux):
    flux.add_cog(Filter(flux))