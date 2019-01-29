import discord
from discord.ext import commands
import mysql.connector
import datetime
import json
from dateutil.relativedelta import relativedelta
from urllib.request import Request, urlopen

class TrainingCommands:
    def __init__(self,bot):
        self.bot = bot
        global hostip
        hostip = bot.hostip
        global requestchannel
        requestchannel = bot.requestchannel
        global noticechannel
        noticechannel = bot.noticechannel
        global tagtoid
        tagtoid = bot.tagtoid

    @commands.command(name='nexttraining', aliases=['nexttrainings'], description='Shows upcoming training sessions.', brief='Shows upcoming training sessions.')
    async def do_nexttraining(self, ctx):
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        IDtrainings = []
        POtrainings = []
        nextIDtrainings = []
        nextPOtrainings = []
        roles=[]
        HR=False
        for i in ctx.author.roles:
            roles.append(i.name)
        if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
            HR = True
        mycursor.execute("SELECT * FROM `trainingsessions` WHERE `TrainingType` = 'Intermediate Driver Training' AND '" + str(datetime.datetime.now() - datetime.timedelta(hours=11) + datetime.timedelta(days=7)) + "' > `TrainingTime` AND `TrainingTime` > '" + str(datetime.datetime.now() - datetime.timedelta(hours=11)) + "'ORDER BY `trainingsessions`.`TrainingTime` ASC;")
        IDtrainings = mycursor.fetchall()
        mycursor.execute("SELECT * FROM `trainingsessions` WHERE `TrainingType` = 'Platform Operator Training' AND '" + str(datetime.datetime.now() - datetime.timedelta(hours=11) + datetime.timedelta(days=7)) + "' > `TrainingTime` AND `TrainingTime` > '" + str(datetime.datetime.now() - datetime.timedelta(hours=11)) + "'ORDER BY `trainingsessions`.`TrainingTime` ASC;")
        POtrainings = mycursor.fetchall()
        # nexttrainingmsg = ['**UPCOMING ID TRAININGS**']
        # for row in IDtrainings:
        #     nexttrainingmsg.append(row[2].strftime('%d/%m/%Y at %I:%M %p. Hosted by: ') + row[3])
        # nexttrainingmsg.append('**UPCOMING PO TRAININGS**')
        # for row in POtrainings:
        #     nexttrainingmsg.append(row[2].strftime('%d/%m/%Y at %I:%M %p. Hosted by: ') + row[3])
        # await ctx.send('\n'.join(nexttrainingmsg))
        for row in IDtrainings:
            try:
                try:
                    host = ctx.guild.get_member(int(row[3])).nick
                    if host == None:
                        raise AttributeError()
                except AttributeError:
                    host = await self.bot.get_user_info(int(row[3]))
                    host = host.name
                except ValueError:
                    host = str(row[3])
            except discord.errors.NotFound:
                host = str(row[3])
            nextIDtrainings.append(row[2].strftime('%d/%m/%Y at %I:%M %p. Hosted by: ') + host + (' [ID: ' + str(row[0]) + ']' if HR == True else ""))
        for row in POtrainings:
            try:
                try:
                    host = ctx.guild.get_member(int(row[3])).nick
                    if host == None:
                        raise AttributeError()
                except AttributeError:
                    host = await self.bot.get_user_info(int(row[3]))
                    host = host.name
                except ValueError:
                    host = str(row[3])
            except discord.errors.NotFound:
                host = str(row[3])
            nextPOtrainings.append(row[2].strftime('%d/%m/%Y at %I:%M %p. Hosted by: ') + host + (' [ID: ' + str(row[0]) + ']' if HR == True else ""))
        nexttrainingmsg = discord.Embed(description='Showing upcoming training sessions up to 1 week from now!', color=3447003)
        nexttrainingmsg.set_author(name='Upcoming Training Sessions', icon_url=self.bot.user.avatar_url)
        nexttrainingmsg.add_field(name='Upcoming ID Trainings', value=('\n'.join(nextIDtrainings) if len(nextIDtrainings) > 0 else '\a'), inline=False)
        nexttrainingmsg.add_field(name='Upcoming PO Trainings', value=('\n'.join(nextPOtrainings) if len(nextPOtrainings) > 0 else '\a'), inline=False)
        nexttrainingmsg.set_footer(icon_url=self.bot.user.avatar_url, text='Nexttraining list generated at: ' + str(datetime.datetime.now() - datetime.timedelta(hours=11)))
        await ctx.send(embed=nexttrainingmsg)

    @commands.command(name='mytrainings', aliases=['mytraining'], description='**SD+ Only** - Displays user\'s or your hosted training sessions.', brief='Displays user\'s or your hosted training sessions.')
    async def do_mytrainings(self, ctx, *tag):
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        if len(tag) > 0:
            user = tagtoid(tag[0], ctx)
        else:
            user = str(ctx.author.id)
        mycursor.execute("SELECT * FROM `trainingsessions` WHERE `Host` = '" + user + "' ORDER BY `trainingsessions`.`TrainingTime` ASC;")
        trainingsessions = mycursor.fetchall()
        hostedtrainingsessions = []
        cohostedtrainingsessions = []
        for row in trainingsessions:
            hostedtrainingsessions.append(row[1] + ' at ' + row[2].strftime('%d/%m/%Y at %I:%M %p'))
        mycursor.execute("SELECT * FROM `trainingsessions` WHERE `Cohost` = '" + user + "' ORDER BY `trainingsessions`.`TrainingTime` ASC;")
        trainingsessions = mycursor.fetchall()
        for row in trainingsessions:
            cohostedtrainingsessions.append(row[1] + ' at ' + row[2].strftime('%d/%m/%Y at %I:%M %p'))
        hostedtrainingmsg = discord.Embed(description='Showing hosted/co-hosted training sessions for: ' + ctx.guild.get_member(int(user)).nick, color=3447003)
        hostedtrainingmsg.set_author(name='Upcoming Training Sessions', icon_url=self.bot.user.avatar_url)
        hostedtrainingmsg.add_field(name='Hosted Trainings', value=(('\n'.join(hostedtrainingsessions)) if len(hostedtrainingsessions) > 0 else '\a'), inline=False)
        hostedtrainingmsg.add_field(name='Co-hosted Trainings', value=('\n'.join(cohostedtrainingsessions) if len(cohostedtrainingsessions) > 0 else '\a'), inline=False)
        hostedtrainingmsg.set_footer(icon_url=self.bot.user.avatar_url, text='Hosted trainings list generated at: ' + str(datetime.datetime.now() - datetime.timedelta(hours=11)))
        await ctx.send(embed=hostedtrainingmsg)

    @commands.command(name='alltrainings', aliases=['alltraining'], description='Displays all training sessions.', brief='Displays all training sessions.')
    async def do_alltrainings(self, ctx):
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        HR=False
        roles = []
        for i in ctx.author.roles:
            roles.append(i.name)
        if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
            HR = True
        mycursor.execute("SELECT * FROM `trainingsessions` ORDER BY `trainingsessions`.`Host` ASC")
        msg = []
        alltrainings = mycursor.fetchall()
        for row in alltrainings:
            try:
                try:
                    host = ctx.guild.get_member(int(row[3])).nick
                    if host == None:
                        raise AttributeError()
                except AttributeError:
                    host = await self.bot.get_user_info(int(row[3]))
                    host = host.name
            except discord.errors.NotFound:
                host = str(row[3])
            try:
                try:
                    cohost = ctx.guild.get_member(int(row[4])).nick
                    if cohost == None:
                        raise AttributeError()
                except AttributeError:
                    cohost = await self.bot.get_user_info(int(row[4]))
                    cohost = cohost.name
                except ValueError:
                    cohost = row[4]
            except discord.errors.NotFound:
                cohost = str(row[4])
            msg.append('**' + row[1] + '**' + row[2].strftime(' at **%I:%M %p** on **%d/%m/%Y**. Hosted by: **') + host + '** Co-hosted by: **' + (cohost if cohost != '' else 'None') + ('** [ID: ' + str(row[0]) + ']' if HR == True else ""))
        await ctx.send('\n'.join(msg))

    @commands.command(name='canceltrainings', aliases=['canceltraining'], description='**SD+ Only** - deletes training session specified.', brief='deletes training session specified.')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_canceltraining(self, ctx, trainingid):
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        mycursor.execute('DELETE FROM `trainingsessions` WHERE `ID` = ' + trainingid)
        AltonDB.commit()
        await ctx.send('Successfully cancelled ' + str(mycursor.rowcount) + ' training session(s)')

    @commands.command(name='trainingreminder', description='**SD+ Only** - Sends a training reminder about the specified training.', brief='Sends a training reminder about the specified training.')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_trainingreminder(self, ctx, trainingid):
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        mycursor.execute('SELECT * FROM trainingsessions')
        for row in mycursor.fetchall():
            if str(row[0]) == trainingid:
                print('FOUND ONE')
                trainingtype = row[1]
                print(trainingtype)
                time = datetime.datetime.strptime(str(row[2])[11:16], '%H:%M')
                posttime = (time - datetime.timedelta(minutes=10)).strftime('%I:%M %p')
                time = str(time.strftime('%I:%M %p'))
                date = str(datetime.datetime.strptime(str(row[2])[:10], '%Y-%m-%d').strftime('%d %B %Y'))
                formattedtime = str(row[2])
                try:
                    try:
                        host = ctx.guild.get_member(int(row[3])).nick
                        if host == None:
                            raise AttributeError()
                    except AttributeError:
                        host = await self.bot.get_user_info(int(row[3]))
                        host = host.name
                except discord.errors.NotFound:
                    host = str(row[3])
                cohost = ''
                if row[4] != '':
                    try:
                        try:
                            cohost = ctx.guild.get_member(int(row[4])).nick
                            if cohost == None:
                                raise AttributeError()
                        except AttributeError:
                            cohost = await self.bot.get_user_info(int(row[4]))
                            cohost = cohost.name
                    except discord.errors.NotFound:
                        cohost = str(row[4])
                TrainingTime = datetime.datetime.strptime(formattedtime, '%Y-%m-%d %H:%M:%S')
                currenttime = str(datetime.datetime.now() - datetime.timedelta(hours=11) - datetime.timedelta(minutes=1))
                currenttime = datetime.datetime.strptime(currenttime, '%Y-%m-%d %H:%M:%S.%f')
                diff = relativedelta(TrainingTime, currenttime)
                if ('Signal' in trainingtype) or ('SG' in trainingtype) or ('Control' in trainingtype) or ('CN' in trainingtype):
                    notifiedrank = 'PLATFORM OPERATORS'
                    trainedrank = 'Controller **[CN]**'
                elif ('Dispatch' in trainingtype) or ('DS' in trainingtype) or ('Platform' in trainingtype) or ('PO' in trainingtype):
                    notifiedrank = 'INTERMEDIATE DRIVERS'
                    trainedrank = 'Platform Operator **[PO]**'
                elif ('Experience' in trainingtype) or ('ED' in trainingtype) or ('Intermediate' in trainingtype) or ('ID' in trainingtype):
                    notifiedrank = 'NOVICE DRIVERS'
                    trainedrank = 'Intermediate Driver **[ID]**'
                elif 'Dev' in trainingtype:
                    trainingtype = 'Developer Training'
                    notifiedrank = 'Trainee Developer'
                    trainedrank = 'Developer'
                else:
                    await ctx.send('Sorry, your trainingtype is not found. Please tell @lucky962#0599, if you would like him to add a new trainingytpe.')
                print('ahsdhfadsf')
                time = time + ' GMT'
                await self.bot.get_channel(noticechannel).send((((((((((((((((((((('Attention **' + notifiedrank) + "**, just a reminder that there'll be a ") + trainedrank) + ' Training in **') + str(diff.days)) + ' days, ') + str(diff.hours)) + ' hours, ') + str(diff.minutes)) + ' minutes  / ') + time) + '!** (') + date) + ') \n\nHost: ') + host) + ((' \nCo-host: ' + cohost) + '\n' if cohost != None else '\n')) + '\nThe link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**') + posttime) + '**].\n\nOnce you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__\n\nThanks for reading,\n**') + ctx.author.nick) + '**')
                await ctx.send('Reminder sent!')

    @commands.command(name='edittraining', description='**SD+ Only** - edits training session specified **Currently in BETA**', brief='edits training session specified **Currently in BETA**')
    @commands.has_any_role('Executive Team','Management Team','High Rank Team')
    async def do_edittraining(self, ctx, trainingid, name, newinfo):
        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        mycursor = AltonDB.cursor(buffered=True)
        await ctx.send('Edittraining command still in early development, there may be a few bugs!')
        print(newinfo)
        if 'co-host' in name.lower() or 'cohost' in name.lower():
            mycursor.execute("UPDATE `trainingsessions` SET `Cohost` = '" + newinfo + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
            AltonDB.commit()
            await ctx.send('Successfully updated Co-host to ' + newinfo)
        elif 'host' in name.lower():
            mycursor.execute("UPDATE `trainingsessions` SET `Host` = '" + newinfo + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
            AltonDB.commit()
            await ctx.send('Successfully updated Host to ' + newinfo)
        elif 'type' in name.lower():
            if ('Dispatch' in newinfo) or ('DS' in newinfo) or ('Platform' in newinfo) or ('PO' in newinfo):
                newinfo = 'Platform Operator Training'
            elif ('Experience' in newinfo) or ('ED' in newinfo) or ('Intermediate' in newinfo) or ('ID' in newinfo):
                newinfo = 'Intermediate Driver Training'
            else:
                await ctx.send('Training type not recognised. Error will most likely occur when posting a training notice.')
            mycursor.execute("UPDATE `trainingsessions` SET `TrainingType` = '" + newinfo + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
            AltonDB.commit()
            await ctx.send('Successfully updated TrainingType to ' + newinfo)
        elif 'time' in name.lower():
            AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
            mycursor = AltonDB.cursor(buffered=True)
            mycursor.execute("SELECT TrainingTime from `trainingsessions` WHERE `trainingsessions`.`ID` = " + trainingid + ";")
            date = datetime.datetime.strptime(str(mycursor.fetchall()[0][0]).split(' ')[0], '%Y-%m-%d').strftime('%d/%m/%Y')
            if ('pm' in newinfo.lower()) or ('am' in newinfo.lower()):
                newinfo = newinfo.replace(' ', '')
                newinfo = (date + ' ') + newinfo
                TrainingTime = datetime.datetime.strptime(newinfo, '%d/%m/%Y %I:%M%p')
            elif (not (':' in newinfo)):
                if len(newinfo) == 4:
                    newinfo = (newinfo[:2] + ':') + newinfo[2:]
                elif len(newinfo) == 3:
                    newinfo = (('0' + newinfo[:1]) + ':') + newinfo[1:]
                newinfo = (date + ' ') + newinfo
                TrainingTime = datetime.datetime.strptime(newinfo, '%d/%m/%Y %H:%M')
            elif ':' in newinfo:
                newinfo = (date + ' ') + newinfo
                TrainingTime = datetime.datetime.strptime(newinfo, '%d/%m/%Y %H:%M')
            TrainingTime = str(TrainingTime)
            mycursor.execute("UPDATE `trainingsessions` SET `TrainingTime` = '" + TrainingTime + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
            AltonDB.commit()
            await ctx.send('Time successfully updated to ' + TrainingTime.split(' ')[1])
        elif 'date' in name.lower():
            AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
            mycursor = AltonDB.cursor(buffered=True)
            mycursor.execute("SELECT TrainingTime from `trainingsessions` WHERE `trainingsessions`.`ID` = " + trainingid + ";")
            date = datetime.datetime.strptime(str(mycursor.fetchall()[0][0]).split(' ')[1], '%H:%M:%S').strftime('%H:%M')
            newinfo = str(datetime.datetime.strptime(newinfo, '%d/%m/%Y').strftime('%Y-%m-%d'))
            date = newinfo + ' ' + date
            mycursor.execute("UPDATE `trainingsessions` SET `TrainingTime` = '" + date + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
            AltonDB.commit()
            await ctx.send('Date successfully updated to ' + date.split(' ')[0] + ' (YYYY-MM-DD)')                    
        else:
            await ctx.send('Sorry, no info found. The syntax is -edittraining [id] [thing to change]: [value to change to]')

    @commands.command(name='endtraining', description='**SD+ Only** Sends a message to training notices that training has ended and automatically promotes users specified. **COMING SOON**', brief='**SD+ Only** Sends a message to training notices that training has ended and automatically promotes users specified. **COMING SOON**')
    async def do_endtraining(self, ctx, trainingid):
        await ctx.send('Endtraining command coming soon! Keep your eyes peeled!')  
        # AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
        # mycursor = AltonDB.cursor(buffered=True)
        # mycursor.execute("SELECT TrainingType from `trainingsessions` WHERE `trainingsessions`.`ID` = " + trainingid + ";")
        # trainingtype = mycursor.fetchall()[0][0]
        # if trainingtype == 'Intermediate Driver Training':
        #     req = Request('https://verify.eryn.io/api/user/' + , headers={'User-Agent': 'Mozilla/5.0'})
        #     webpage = urlopen(req).read()
        #     webpage = json.loads(webpage.decode())
        #     robloxid = webpage.get('robloxId')
        # elif trainingtype == 'Platform Operator Training':

def setup(bot):
    bot.add_cog(TrainingCommands(bot))