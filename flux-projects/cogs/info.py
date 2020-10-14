import discord
from discord.ext import commands
from util.config_manager import read as config
from util.db_manager import db_connection
import asyncio


class Info(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.command(brief='View information about a specific project.', help='View all information about the specified project or the latest project to be created if no project ID is is specified.')
    @commands.guild_only()
    async def info(self, ctx, id: int = None):
        content = ""

        # No project was specified, we'll send the latest one and a message to signify this.
        if id is None:
            id = await self.get_latest_project_ID()
            content = "This is the latest project:"

        # Request data relating to the specified project
        with db_connection() as db:
            db.execute(f'SELECT * FROM `projects` WHERE `id` = \'{id}\' LIMIT 1')
            project = db.fetchone()

        # No data was returned, there is no project by the ID that was specified
        if project is None:
            await ctx.message.delete()
            return await ctx.send(f'{ctx.author.mention}, There are no projects by the ID `{id}`.', delete_after=10)
        
        # Form the returned data and send it
        data = await self.form_project_data(ctx, project, 'short')
        msg = await ctx.send(content=content, embed=data)

        '''
        The remainder of this function handles the temporary solution to send further information about a project.
        '''

        await msg.add_reaction('ℹ️')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == 'ℹ️'

        try:
            reaction, user = await self.flux.wait_for('reaction_add', timeout=60.0, check=check)

        except asyncio.TimeoutError:
            pass

        else:
            data = await self.form_project_data(ctx, project, 'longer')
            await ctx.author.send(embed=data)
        
        finally:
            await msg.clear_reactions()

    async def get_latest_project_ID(self):
        with db_connection() as db:
            db.execute('SELECT id FROM `projects` ORDER BY `projects`.`id` DESC LIMIT 1')
            project_ID = db.fetchone()
            return project_ID[0]

    async def form_project_data(self, ctx, data: tuple, detail: str = 'short'):
        
        colour = await commands.ColourConverter.convert(self, ctx, config(('Objectives', str(data[7])))[1]) if data[7] != None else discord.Colour(0x202225)

        embed = discord.Embed(title=data[1], description=data[4], colour=colour)

        if data[8] != None:
            leader = await self.get_member_then_user(ctx, data[8])
        else:
            # There was no data from the DB, don't bother trying to retrieve the member or user object
            leader = None

        embed.set_author(name=leader.display_name, icon_url=leader.avatar_url) if leader != None else embed

        embed.set_footer(text=f'Project ID #{data[0]}  |  Flux {"Official" if data[10] else "Volunteer"} Project')

        # Conditional fields

        embed.add_field(name='Objective', value=config(('Objectives', str(data[7])))[0] if data[7] else None, inline=True) if detail == "long" or detail == "longer" else embed
        embed.add_field(name='Completion', value=data[3], inline=True) if detail == "long" or detail == "longer" else embed
        embed.add_field(name='Status', value=config(('Status', str(data[11]))), inline=True) if detail == "long" or detail == "longer" else embed

        if detail == "longer":
            if data[9]:
                resources = ''
                for i in data[9]:
                    resource_holder = await self.get_member_then_user(ctx, config(('Resources', i))[1])
                    resources += f"{config(('Resources', i))[0]} - {resource_holder.display_name}\n"
            else:
                resources = None
        embed.add_field(name='Resouces', value=resources, inline=True) if detail == "longer" else embed
        embed.add_field(name='Outcomes', value=data[5], inline=True) if detail == "longer" else embed
        embed.add_field(name='Deliverables', value=data[6], inline=True) if detail == "longer" else embed

        return embed
    
    # Attempt to get a member object in context, fallback to user object
    async def get_member_then_user(self, ctx, id):
        object = ctx.guild.get_member(id)
        if object == None:
            object = await self.flux.fetch_user(id)
            
        return object


def setup(flux):
    flux.add_cog(Info(flux))