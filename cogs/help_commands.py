import discord
from discord.ext import commands

class HelpCommands:
    def __init__(self,bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def do_help(self, ctx):
        if ctx.invoked_subcommand is None:
            HelpMsg = discord.Embed(title='Help Page', description='There are two types of commands you can use with AltonBot. \nPlease type ' + '-' + 'help [type] to see help for a certain type of command', color=3447003)
            HelpMsg.set_author(name='Alton Bot', icon_url=bot.user.avatar_url)
            HelpMsg.add_field(name='Moderation', value='This includes all the commands that warn, ban and kick users.')
            HelpMsg.add_field(name='Trainings', value='This includes all the commands that the bot can do in regards to trainings')
            HelpMsg.add_field(name='Other', value='This includes any other commands that AltonBot can do')
            HelpMsg.set_footer(icon_url=bot.user.avatar_url, text='© Alton County Railways')
            await ctx.send(embed=HelpMsg)

    @help.command(name='moderation')
    async def do_help_moderation(self, ctx):
        HelpMsg = discord.Embed(title='Help Page', description='This is a page full of moderation commands you can use with AltonBot', color=3447003)
        HelpMsg.set_author(name='Alton Bot', icon_url=bot.user.avatar_url)
        HelpMsg.add_field(name=('-' + 'warn [user]', value='**SD+ Only** - warns a user')
        HelpMsg.add_field(name=('-' + 'kick [user]', value='**SD+ Only** - kicks a user')
        HelpMsg.add_field(name=('-' + 'ban [user]', value='**MOD+ Only** - bans a user indefinetely or until unbanned.')
        HelpMsg.add_field(name=('-' + 'warnings [user(optional)]', value='Displays all warnings currently stored in memory or just for the user.')
        HelpMsg.add_field(name=('-' + 'clearwarnings [user]', value='**SD+ Only** - clears the warnings of a certain player.')
        HelpMsg.set_footer(icon_url=bot.user.avatar_url, text='© Alton County Railways')
        await ctx.send(embed=HelpMsg)

    @help.command(name='training')
    async def do_help_training(self, ctx):
        HelpMsg = discord.Embed(title='Help Page', description='This is a page full of training commands you can use with AltonBot', color=3447003)
        HelpMsg.set_author(name='Alton Bot', icon_url=bot.user.avatar_url)
        HelpMsg.add_field(name=('-' + 'nexttrainings', value='Shows upcoming training sessions.')
        HelpMsg.add_field(name=('-' + 'trainingreminder [id]', value='**SD+ Only** - Sends a training reminder about the specified training.')
        HelpMsg.add_field(name=('-' + 'edittraining [id] [fieldtochange]: [valuetochangeto]', value='**SD+ Only** - edits training session specified **Currently in BETA**')
        HelpMsg.add_field(name=('-' + 'canceltraining [id]', value='**SD+ Only** - deletes training session specified.')
        HelpMsg.add_field(name=('-' + 'mytrainings [user(optional)]', value='**SD+ Only** - Displays user\'s or your hosted training sessions.')
        HelpMsg.add_field(name=('-' + 'alltrainings', value='Displays all training sessions.')
        HelpMsg.add_field(name=('-' + 'endtraining [id] [passeduser1] [passeduser2]...', value='**SD+ Only** Sends a message to training notices that training has ended and automatically promotes users specified. **COMING SOON**')
        HelpMsg.set_footer(icon_url=bot.user.avatar_url, text='© Alton County Railways')
        await ctx.send(embed=HelpMsg)
        
    @help.command(name='other')
    async def do_help_other(self, ctx):
        HelpMsg = discord.Embed(title='Help Page', description='This is a page full of other commands you can use with AltonBot', color=3447003)
        HelpMsg.set_author(name='Alton Bot', icon_url=bot.user.avatar_url)
        HelpMsg.add_field(name=('-' + 'help', value='Displays a help page.')
        HelpMsg.add_field(name=('-' + 'prefix', value='Changes the prefix for commands')
        HelpMsg.set_footer(icon_url=bot.user.avatar_url, text='© Alton County Railways')
        await ctx.send(embed=HelpMsg)

def setup(bot):
    bot.add_cog(HelpCommands(bot))