import discord
from discord.ext import commands

class OtherCommands:
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name='await', description='**lucky962 only** does a raw await command', brief='**lucky962 only** does a raw await command', hidden=True)
    @commands.is_owner()
    async def do_setprefix(self, ctx, *, args):
        await ctx.message.delete()
        await eval(args)

    @commands.command(name='echo', description='**lucky962 only** does a raw await command', brief='**lucky962 only** does a raw await command', hidden=True)
    @commands.has_any_role('Executive Team','Management Team')
    async def do_echo   (self, ctx, *, args):
        await ctx.message.delete()
        await ctx.send(args)
    # @commands.command(name='setprefix', description='**MOD+** changes the prefix for this bot', brief='changes the prefix for this bot')
    # @commands.has_any_role('Executive Team','Management Team')


def setup(bot):
    bot.add_cog(OtherCommands(bot))