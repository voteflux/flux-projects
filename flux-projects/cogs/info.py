import discord
from discord.ext import commands
from utility.config_manager import read as config
from utility.db_manager import db_connection
import asyncio


class Info(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='View information about a specific project.', help='View all information about the specified project or the latest project to be created if no project ID is is specified.')
    @commands.guild_only()
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

        colour = await commands.ColourConverter.convert(self, ctx, config(('Objectives', str(project[7])))[1])

        embed = discord.Embed(title=project[1], description=project[4], colour=colour)
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        embed.add_field(name='Objective', value=config(('Objectives', str(project[7])))[0], inline=True)
        embed.add_field(name='Completion', value=project[3], inline=True)
        embed.add_field(name='Status', value=config(('Status', str(project[11]))), inline=True)
        embed.set_footer(text=f'Project ID #{project[0]}  |  Flux {"Official" if project[10] else "Volunteer"} Project')

        msg = await ctx.send(content=content, embed=embed)
        
        await msg.add_reaction('ℹ️')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == 'ℹ️'

        try:
            reaction, user = await self.flux.wait_for('reaction_add', timeout=60.0, check=check)

        except asyncio.TimeoutError:
            pass

        else:
            content = "Here is some further information about the project:"
            embed = discord.Embed(title=project[1], description=project[4], colour=colour)
            embed.set_author(name=author.display_name, icon_url=author.avatar_url)
            embed.add_field(name='Objective', value=config(('Objectives', str(project[7])))[0], inline=True)
            embed.add_field(name='Completion', value=project[3], inline=True)
            embed.add_field(name='Status', value=config(('Status', str(project[11]))), inline=True)
            embed.add_field(name='Resouces', value=project[9], inline=True)
            embed.add_field(name='Outcomes', value=project[5], inline=True)
            embed.add_field(name='Deliverables', value=project[6], inline=True)
            embed.set_footer(text=f'Project ID #{project[0]}  |  Flux {"Official" if project[10] else "Volunteer"} Project')
            await ctx.author.send(content=content, embed=embed)
        
        finally:
            await msg.clear_reactions()

    async def get_latest_project_ID(self):
        with db_connection() as db:
            db.execute('SELECT id FROM `projects` ORDER BY `projects`.`id` DESC LIMIT 1')
            project_ID = db.fetchone()
            return project_ID[0]

    async def send_project_info(self, ctx, data: tuple, detail: str = 'short'):
        
        colour = await commands.ColourConverter.convert(self, ctx, config(('Objectives', str(data[7])))[1]) if data[7] != None else discord.Colour(0x202225)

        embed = discord.Embed(title=data[1], description=data[4], colour=colour)

        if data[8] != None:
            leader = ctx.guild.get_member(data[8])
            if leader == None:
                # API request for a User object instead of a Member object incase the user is not in the guild
                leader = await self.flux.fetch_user(data[8])
        else:
            # There was no data from the DB, don't bother trying to retrieve the member or user object
            leader = None

        embed.set_author(name=leader.display_name, icon_url=leader.avatar_url) if leader != None else embed

        embed.set_footer(text=f'Project ID #{data[0]}  |  Flux {"Official" if data[10] else "Volunteer"} Project')

        # Conditional fields

        embed.add_field(name='Objective', value=config(('Objectives', str(data[7])))[0], inline=True) if detail == "long" or detail == "longer" else embed
        embed.add_field(name='Completion', value=data[3], inline=True) if detail == "long" or detail == "longer" else embed
        embed.add_field(name='Status', value=config(('Status', str(data[11]))), inline=True) if detail == "long" or detail == "longer" else embed

        embed.add_field(name='Resouces', value=data[9], inline=True) if detail == "longer" else embed
        embed.add_field(name='Outcomes', value=data[5], inline=True) if detail == "longer" else embed
        embed.add_field(name='Deliverables', value=data[6], inline=True) if detail == "longer" else embed

        message = await ctx.channel.send(embed=embed)
        return message


def setup(flux):
    flux.add_cog(Info(flux))