import discord
from discord.ext import commands
import mysql.connector

class TrainingCommands:
    def __init__(self,bot):
        self.bot = bot
        global hostip
        hostip = bot.hostip

    @commands.command(name='canceltrainings', aliases=['canceltraining'])
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_canceltraining(self, ctx, trainingid):
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        mycursor.execute('DELETE FROM `trainingsessions` WHERE `ID` = ' + trainingid)
        AltonDB.commit()
        await ctx.send('Successfully cancelled ' + str(mycursor.rowcount) + ' training session(s)')

def setup(bot):
    bot.add_cog(TrainingCommands(bot))