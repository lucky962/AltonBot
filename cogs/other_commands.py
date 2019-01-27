import discord
from discord.ext import commands

class OtherCommands:
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name='await', description='**lucky962 only** does a raw await command', brief='**lucky962 only** does a raw await command')
    @commands.is_owner()
    async def do_setprefix(self, ctx, *, args):
        await ctx.message.delete()
        await eval(args)

def setup(bot):
    bot.add_cog(OtherCommands(bot))