import traceback
import sys
from discord.ext import commands
import discord


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.errors.CheckFailure):
            return await ctx.send('You don\'t have enough permissions to run this command')
        
        elif isinstance(error, commands.errors.DisabledCommand):
            return await ctx.send('This command has been disabled, please dm lucky9621 if you think this has been an error.')

        await ctx.send(traceback.format_exception(type(error), error, error.__traceback__)[-1])  
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    # @commands.command(name='repeat', aliases=['mimic', 'copy'])
    # async def do_repeat(self, ctx, *, inp: str):
    #     await ctx.send(inp)

    # @do_repeat.error
    # async def do_repeat_handler(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         if error.param.name == 'inp':
    #             await ctx.send("You forgot to give me input to repeat!")
                

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
