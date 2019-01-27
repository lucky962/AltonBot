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

    @commands.command(name='warn', description='**SD+ Only** - warns a user', brief='warns a user')
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


    @commands.command(name='kick', description='**SD+ Only** - kicks a user', brief='kicks a user')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_kick(self, ctx, tag, *, reason):
        try:
            tag = tagtoid(tag, ctx)
            await ctx.send(((('<@' + tag) + '> has been kicked for: ') + reason) + '.')
            try:
                await ctx.guild.get_member(int(tag)).send('You have been kicked from Alton County Railways for: ' + reason)
            except discord.errors.Forbidden:
                pass
            await ctx.guild.kick(ctx.guild.get_member(int(tag)), reason=reason)
        except discord.errors.Forbidden:
            await ctx.send('I do not have permission to kick this user.')
    @do_kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('A reason is needed to kick.')

    @commands.command(name='ban', description='**SD+ Only** - bans a user', brief='bans a user')
    @commands.has_any_role('Executive Team','Management Team')
    async def do_ban(self, ctx, tag, *, reason):
        tag = tagtoid(tag, ctx)
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        try:
            await ctx.send(((('<@' + tag) + '> has been banned for: ') + reason) + '.')
            try:
                await ctx.guild.get_member(int(tag)).send('You have been banned from Alton County Railways for: ' + reason)
            except discord.errors.Forbidden:
                pass
            except AttributeError:
                pass
            await ctx.guild.ban(ctx.guild.get_member(int(tag)), reason=reason)
            mycursor.execute("INSERT INTO banlist (Banned, Banner, Reason) VALUES ('" + tag + "', '" + str(ctx.author.id) + "', '" + reason + "');")
            AltonDB.commit()
        except discord.errors.Forbidden:
            await ctx.send('I do not have permissions to ban this user.')
    @do_ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('A reason is needed to ban.')
        

    @commands.command(name='warnings', description='Displays all warnings currently stored in memory or just for the user.', brief='Displays all warnings currently stored in memory.')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_warnings(self, ctx, *tag):
        msg = []
        search = ''
        print(tag)
        if len(tag) > 0:
            search = " WHERE `Warned` = " + tagtoid(tag[0], ctx)
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        mycursor.execute("SELECT * FROM `warnlist`" + search + " ORDER BY `warnlist`.`Warned` ASC")
        warnings  = mycursor.fetchall()
        print(warnings)
        for row in warnings:
            print(row)
            try:
                try:
                    warned = ctx.guild.get_member(int(row[1])).nick
                    if warned == None:
                        raise AttributeError()
                except AttributeError:
                    warned = await self.bot.get_user_info(int(row[1]))
                    warned = warned.name
            except discord.errors.NotFound:
                warned = str(row[1])
            try:
                try:
                    warner = ctx.guild.get_member(int(row[2])).nick
                    if warner == None:
                        raise AttributeError()
                except AttributeError:
                    warner = await self.bot.get_user_info(int(row[2]))
                    warner = warner.name
            except discord.errors.NotFound:
                warner = str(row[2])
            print('*' + warned + '* was warned by *' + warner + '* for reason: ' + row[3])
            msg.append('*' + warned + '* was warned by *' + warner + '* for reason: ' + row[3])
        try:
            await ctx.send('\n'.join(msg))
        except discord.errors.HTTPException:
            await ctx.send('This user has no warnings.')

    @commands.command(name='clearwarnings', aliases=['clearwarn','clearwarning','clearwarns'], description='**SD+ Only** - clears the warnings of a certain player.', brief='clears the warnings of a certain player.')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_clearwarnings(self, ctx, tag):
        tag = tagtoid(tag, ctx)
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        mycursor.execute("DELETE FROM `warnlist` WHERE `warned` = '" + tag + "'")
        noofwarns = mycursor.rowcount
        AltonDB.commit()
        try:
            nickname = ctx.guild.get_member(int(tag)).nick
        except AttributeError:
            try:
                nickname = await self.bot.get_user_info(int(tag))
                nickname = nickname.name
            except discord.errors.NotFound:
                nickname = str(tag)
        if nickname == None:
            nickname = await self.bot.get_user_info(int(tag))
            nickname = nickname.name
        await ctx.send('Successfully cleared ' + str(noofwarns) + ' warnings for ' + nickname)


def setup(bot):
    bot.add_cog(ModerationCommands(bot))