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

    @commands.command(name='membercount', description='Counts the amount of members in this server', brief='Counts the amount of members in this server')
    async def do_membercount(self, ctx):
        print(ctx.guild.members)
        members = 0
        onlinemembers = 0
        humans = 0
        bots = 0
        for i in ctx.guild.members:
            members += 1
            print(i.status)
            print(type(i.status))
            if i.status != discord.Status('offline'):
                onlinemembers += 1
            if i.bot == True:
                bots += 1
            elif i.bot == False:
                humans += 1
        membercount=discord.Embed()
        membercount.add_field(name='Members', value=members, inline=False)
        membercount.add_field(name='Online', value=onlinemembers, inline=False)
        membercount.add_field(name='Humans', value=humans, inline=False)
        membercount.add_field(name='Bots', value=bots, inline=False)
        await ctx.send(embed=membercount)

    @commands.command(name='purge', description='**SD+ Only** - deletes number of messages specified', brief='deletes number of messages  specified')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_purge(self, ctx, noofmessages):
        await ctx.channel.purge(limit=int(noofmessages) + 1)

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

    @commands.command(name='mute')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_mute(self, ctx, tag):
        tag = tagtoid(tag, ctx)
        print(tag)
        member = ctx.guild.get_member(int(tag))
        print(member)
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(role)
        await ctx.send(str(member.nick) + ' was muted by ' + ctx.message.author.nick)

    @commands.command(name='unmute')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_unmute(self, ctx, tag):
        tag = tagtoid(tag, ctx)
        print(tag)
        member = ctx.guild.get_member(int(tag))
        print(member)
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role)
        await ctx.send(str(member.nick) + ' was unmuted by ' + ctx.message.author.nick)

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
        await ctx.channel.trigger_typing()
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
            msg.append('*' + warned + '* was warned by *' + warner + '* for reason: ' + row[3])
        msg = '\n'.join(msg)
        print(msg)
        if len(msg) > 2000:
            msg = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
            print(msg)
            for i in msg:
                await ctx.send(i)
        elif len(msg) > 0:
            await ctx.send(msg)
        else:
            tag = tagtoid(tag[0], ctx)
            try:
                try:
                    user = ctx.guild.get_member(int(tag)).nick
                    if user == None:
                        raise AttributeError()
                except AttributeError:
                    user = await self.bot.get_user_info(int(tag))
                    user = user.name
            except discord.errors.NotFound:
                user = str(tag)
            await ctx.send(user + ' has no warnings.')

    @commands.command(name='clearwarnings', aliases=['clearwarn','clearwarning','clearwarns'], description='**SD+ Only** - clears the warnings of a certain player.', brief='clears the warnings of a certain player.')
    @commands.has_any_role('Executive Team','Management Team')
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