import discord
from discord.ext import commands


class Error_Handling(commands.Cog):

    def __init__(self, flux):
        self.flux = flux

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'Invalid command. See {await self.flux.get_prefix(ctx)}help')

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Insufficient permissions')

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Missing argument. See {await self.flux.get_prefix(ctx)}help')

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f'{ctx.author.mention}, you can\'t use this command in a private message. Head to the bot channel.')

        elif isinstance(error, commands.MissingRole):
            await ctx.send('You don\'t have the required role.')

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send('{ctx.author.mention} You must wait a minute to use this command again.')

        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(f'{ctx.author.mention} You can only run this command once at a time.')

        else:
            await ctx.send(f'Uh oh... something broke again. Stand by for an admin.')
            print(f'\n\nCOMMAND ERROR:\nAuthor: {ctx.author}\nChannel: {ctx.channel}\nCommand: {ctx.message.content}\n{error}\n\n')


def setup(flux):
    flux.add_cog(Error_Handling(flux))