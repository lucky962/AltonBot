import discord
from discord.ext import commands
import mysql.connector

class ModerationCommands:
    def __init__(self,bot):
        self.bot = bot
        global hostip
        global tagtoid
        hostip = bot.hostip
        tagtoid = bot.tagtoid

    @commands.command(name='warn')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_warn(self, ctx, warned, *, reason):
        warned = tagtoid(warned, ctx)
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        print(warned)
        print(reason)
        mycursor.execute("INSERT INTO warnlist (Warned, Warner, Reason) VALUES ('" + warned + "', '" + str(ctx.author.id) + "', '" + reason + "');")
        AltonDB.commit()
        mycursor.execute("SELECT * FROM `warnlist` WHERE `Warned` = '" + warned + "'")
        noofwarns = mycursor.rowcount
        await ctx.send((((('<@' + warned) + '> has been warned for: ') + reason) + '. This is warning number ') + str(noofwarns))
        try:
            await ctx.guild.get_member(int(warned)).send('You have been warned from Alton County Railways for: ' + reason)
        except discord.errors.Forbidden:
            pass
        if (noofwarns == 3) or (noofwarns == 6):
            try:
                await ctx.send(((('<@' + warned) + '> will now be kicked for having ') + str(noofwarns)) + ' warnings.')
                try:
                    await ctx.guild.get_member(int(warned)).send(('You have been kicked from Alton County Railways for having ' + str(noofwarns)) + ' warnings.')
                except discord.errors.Forbidden:
                    pass
                await ctx.guild.kick(ctx.guild.get_member(int(warned)), reason=str(noofwarns) + ' warnings')
            except discord.errors.Forbidden:
                await ctx.send("Sorry, I don't have the permissions to kick that user.")
        elif (noofwarns > 8):
            try:
                await ctx.send(((('<@' + warned) + '> will now be banned for having ') + str(noofwarns)) + ' warnings.')
                try:
                    await ctx.guild.get_member(int(warned)).send(('You have been banned from Alton County Railways for having ' + str(noofwarns)) + ' warnings.')
                except discord.errors.Forbidden:
                    pass
                await ctx.guild.ban(ctx.guild.get_member(int(warned)), reason=str(noofwarns) + ' warnings')
                mycursor.execute("INSERT INTO warnlist (Banned, Banner, Reason) VALUES ('" + warned + "', '" + str(ctx.author.id) + "', '" + str(noofwarns) + " warnings');")
                AltonDB.commit()
            except discord.errors.Forbidden:
                await ctx.send("Sorry, I don't have the permissions to ban that user.")

def setup(bot):
    bot.add_cog(ModerationCommands(bot))