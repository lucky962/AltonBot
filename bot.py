import discord
import os
import re
import datetime
import mysql.connector
import time
import asyncio
import traceback
from dateutil.relativedelta import relativedelta
from Dependencies.ServerPrefixes import *
from discord.ext import *
print(CMDPrefix)
with open('BotToken.txt') as f:
    TOKEN = f.read()
hostip = 'localhost'
AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
noticechannel = 520701561564037143
requestchannel = 528528451192356874
guildid = 514155943525875716
mycursor = AltonDB.cursor(buffered=True)
os.chdir('Dependencies')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=(CMDPrefix.get(514155943525875716) if 514155943525875716 in CMDPrefix else '!') + 'help'))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        print('automaticreminder task started')
        await self.wait_until_ready()
        print('client is ready')
        guild = self.get_guild(guildid)
        gameplaying = 0
        while not self.is_closed():
            if gameplaying == 0:
                await self.change_presence(activity=discord.Game(name='Alton County Railways'))
                gameplaying = 1
            elif gameplaying == 1:
                await self.change_presence(activity=discord.Game(name=(CMDPrefix.get(514155943525875716) if 514155943525875716 in CMDPrefix else '!') + 'help'))
                gameplaying = 0
            AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
            mycursor = AltonDB.cursor(buffered=True)
            mycursor.execute("SELECT * FROM `trainingsessions` WHERE `TrainingTime` > '" + str(datetime.datetime.now() - datetime.timedelta(hours=11)) + "' AND `TrainingTime` < '" + str(datetime.datetime.now() - datetime.timedelta(hours=10)) + "' AND `Reminded` = 0")
            trainingreminders = mycursor.fetchall()
            for row in trainingreminders:
                print(row)
                trainingtype = row[1]
                print(trainingtype)
                time = datetime.datetime.strptime(str(row[2])[11:16], '%H:%M')
                posttime = (time - datetime.timedelta(minutes=10)).strftime('%I:%M %p')
                time = str(time.strftime('%I:%M %p'))
                date = str(datetime.datetime.strptime(str(row[2])[:10], '%Y-%m-%d').strftime('%d %B %Y'))
                formattedtime = str(row[2])
                try:
                    try:
                        host = guild.get_member(int(row[3])).nick
                        if host == None:
                            raise AttributeError()
                    except AttributeError:
                        host = await self.get_user_info(int(row[3]))
                        host = host.name
                except discord.errors.NotFound:
                    host = str(row[3])
                if row[4] != '':
                    try:
                        int(row[4])
                        try:
                            try:
                                cohost = guild.get_member(int(row[4])).nick
                                if cohost == None:
                                    raise AttributeError()
                            except AttributeError:
                                cohost = await self.get_user_info(int(row[4]))
                                cohost = cohost.name
                        except discord.errors.NotFound:
                            cohost = str(row[4])
                    except ValueError:
                        cohost = row[4]
                else:
                    cohost = ''
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
                time = time + ' GMT'
                await self.get_channel(noticechannel).send('Attention **' + notifiedrank + "**, just a reminder that there'll be a " + trainedrank + ' Training in **' + str(diff.days) + ' days, ' + str(diff.hours) + ' hours, ' + str(diff.minutes) + ' minutes  / ' + time + '!** (' + date + ') \n\nHost: ' + host + ' \nCo-host: ' + ((cohost + '\n') if cohost != '' else '\n') + '\nThe link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**' + posttime + '**].\n\nOnce you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__\n\nThanks for reading,\n**' + host + '**')
                mycursor.execute("UPDATE `trainingsessions` SET `Reminded` = '1' WHERE `trainingsessions`.`ID` = " + str(row[0]) + ";")
                AltonDB.commit()
                print('done')
            await asyncio.sleep(10)

client = MyClient()

def tagtoid(tag, message): # Changes discord tag to id
    try:
        isd = int(tag.lstrip('<@!').lstrip('<@').rstrip('>'))
        return (str(isd))
    except ValueError:
        members = message.guild.members
        print(members)
        member = []
        for i in members:
            print(i)
            if i.nick == None:
                if tag.lower() in i.name.lower():
                    member.append(i.id)
                    print('no nickname matching name')
                continue
            if tag.lower() in i.nick.lower():
                member.append(i.id)
            elif tag.lower() in i.name.lower():
                member.append(i.id)
        if len(member) == 0:
            return None
        else:
            return(str(member[0]))

@client.event
async def on_message(message):
    print(message.author)
    print(message.content)
    try:
        if message.author == client.user:
            return
        if message.content.startswith(CMDPrefix.get(message.guild.id)):
            await message.channel.trigger_typing()
            print('COMMAND DETECTED')
            messege = message.content[len(CMDPrefix.get(message.guild.id)):]
            if messege.startswith('hello'):
                msg = 'Hello {0.author.mention}'.format(message)
                await message.channel.send(msg)
            elif messege.startswith('trainingreminder '):
                roles = []
                for i in message.author.roles:
                    roles.append(i.name)
                print(roles)
                if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                    print('TRAININGREMINDER')
                    trainingid = (messege[17:])
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
                                    host = message.guild.get_member(int(row[3])).nick
                                    if host == None:
                                        raise AttributeError()
                                except AttributeError:
                                    host = await client.get_user_info(int(row[3]))
                                    host = host.name
                            except discord.errors.NotFound:
                                host = str(row[3])
                            cohost = ''
                            if row[4] != '':
                                try:
                                    try:
                                        cohost = message.guild.get_member(int(row[4])).nick
                                        if cohost == None:
                                            raise AttributeError()
                                    except AttributeError:
                                        cohost = await client.get_user_info(int(row[4]))
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
                                await message.channel.send('Sorry, your trainingtype is not found. Please tell @lucky962#0599, if you would like him to add a new trainingytpe.')
                            print('ahsdhfadsf')
                            time = time + ' GMT'
                            await client.get_channel(noticechannel).send((((((((((((((((((((('Attention **' + notifiedrank) + "**, just a reminder that there'll be a ") + trainedrank) + ' Training in **') + str(diff.days)) + ' days, ') + str(diff.hours)) + ' hours, ') + str(diff.minutes)) + ' minutes  / ') + time) + '!** (') + date) + ') \n\nHost: ') + host) + ((' \nCo-host: ' + cohost) + '\n' if cohost != None else '\n')) + '\nThe link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**') + posttime) + '**].\n\nOnce you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__\n\nThanks for reading,\n**') + message.author.nick) + '**')
                            await message.channel.send('Reminder sent!')
            elif messege.startswith('canceltraining '):
                roles = []
                for i in message.author.roles:
                    roles.append(i.name)
                print(roles)
                if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                    trainingid = messege[15:]
                    AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                    mycursor = AltonDB.cursor(buffered=True)
                    mycursor.execute('DELETE FROM `trainingsessions` WHERE `ID` = ' + trainingid)
                    AltonDB.commit()
                    await message.channel.send('Successfully cancelled ' + str(mycursor.rowcount) + ' training session(s)')
            elif messege.startswith('edittraining'):
                roles = []
                for i in message.author.roles:
                    roles.append(i.name)
                print(roles)
                if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                    AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                    mycursor = AltonDB.cursor(buffered=True)
                    await message.channel.send('Edittraining command still in early development, there may be a few bugs!')
                    trainingid = (messege.split(' '))[1]
                    part = message.content.split(':', maxsplit=1)
                    newinfo = part[1].strip(' ')
                    print(newinfo)
                    if 'co-host' in messege.lower() or 'cohost' in messege.lower():
                        mycursor.execute("UPDATE `trainingsessions` SET `Cohost` = '" + newinfo + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
                        AltonDB.commit()
                        await message.channel.send('Successfully updated Co-host to ' + newinfo)
                    elif 'host' in messege.lower():
                        mycursor.execute("UPDATE `trainingsessions` SET `Host` = '" + newinfo + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
                        AltonDB.commit()
                        await message.channel.send('Successfully updated Host to ' + newinfo)
                    elif 'type' in messege.lower():
                        if ('Dispatch' in newinfo) or ('DS' in newinfo) or ('Platform' in newinfo) or ('PO' in newinfo):
                            newinfo = 'Platform Operator Training'
                        elif ('Experience' in newinfo) or ('ED' in newinfo) or ('Intermediate' in newinfo) or ('ID' in newinfo):
                            newinfo = 'Intermediate Driver Training'
                        else:
                            await message.channel.send('Training type not recognised. Error will most likely occur when posting a training notice.')
                        mycursor.execute("UPDATE `trainingsessions` SET `TrainingType` = '" + newinfo + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
                        AltonDB.commit()
                        await message.channel.send('Successfully updated TrainingType to ' + newinfo)
                    elif 'time' in messege.lower():
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
                                newinfo = time = (newinfo[:2] + ':') + newinfo[2:]
                            elif len(newinfo) == 3:
                                newinfo = time = (('0' + newinfo[:1]) + ':') + newinfo[1:]
                            newinfo = (date + ' ') + newinfo
                            TrainingTime = datetime.datetime.strptime(newinfo, '%d/%m/%Y %H:%M')
                        elif ':' in newinfo:
                            newinfo = (date + ' ') + newinfo
                            TrainingTime = datetime.datetime.strptime(newinfo, '%d/%m/%Y %H:%M')
                        TrainingTime = str(TrainingTime)
                        mycursor.execute("UPDATE `trainingsessions` SET `TrainingTime` = '" + TrainingTime + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
                        AltonDB.commit()
                        await message.channel.send('Time successfully updated to ' + TrainingTime.split(' ')[1])
                    elif 'date' in messege.lower():
                        AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                        mycursor = AltonDB.cursor(buffered=True)
                        mycursor.execute("SELECT TrainingTime from `trainingsessions` WHERE `trainingsessions`.`ID` = " + trainingid + ";")
                        date = datetime.datetime.strptime(str(mycursor.fetchall()[0][0]).split(' ')[1], '%H:%M:%S').strftime('%H:%M')
                        newinfo = str(datetime.datetime.strptime(newinfo, '%d/%m/%Y').strftime('%Y-%m-%d'))
                        date = newinfo + ' ' + date
                        mycursor.execute("UPDATE `trainingsessions` SET `TrainingTime` = '" + date + "' WHERE `trainingsessions`.`ID` = " + trainingid + ";")
                        AltonDB.commit()
                        await message.channel.send('Date successfully updated to ' + date.split(' ')[0] + ' (YYYY-MM-DD)')                    
                    else:
                        await message.channel.send('Sorry, no info found. The syntax is -edittraining [id] [thing to change]: [value to change to]')
                else: 
                    await message.channel.send('Sorry, you have to be an SD+ to edit trainings.')
            elif messege.startswith('nexttraining'):
                AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                mycursor = AltonDB.cursor(buffered=True)
                IDtrainings = []
                POtrainings = []
                nextIDtrainings = []
                nextPOtrainings = []
                roles=[]
                HR=False
                for i in message.author.roles:
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
                # await message.channel.send('\n'.join(nexttrainingmsg))
                for row in IDtrainings:
                    try:
                        try:
                            host = message.guild.get_member(int(row[3])).nick
                            if host == None:
                                raise AttributeError()
                        except AttributeError:
                            host = await client.get_user_info(int(row[3]))
                            host = host.name
                        except ValueError:
                            host = str(row[3])
                    except discord.errors.NotFound:
                        host = str(row[3])
                    nextIDtrainings.append(row[2].strftime('%d/%m/%Y at %I:%M %p. Hosted by: ') + host + (' [ID: ' + str(row[0]) + ']' if HR == True else ""))
                for row in POtrainings:
                    try:
                        try:
                            host = message.guild.get_member(int(row[3])).nick
                            if host == None:
                                raise AttributeError()
                        except AttributeError:
                            host = await client.get_user_info(int(row[3]))
                            host = host.name
                        except ValueError:
                            host = str(row[3])
                    except discord.errors.NotFound:
                        host = str(row[3])
                    nextPOtrainings.append(row[2].strftime('%d/%m/%Y at %I:%M %p. Hosted by: ') + host + (' [ID: ' + str(row[0]) + ']' if HR == True else ""))
                nexttrainingmsg = discord.Embed(description='Showing upcoming training sessions up to 1 week from now!', color=3447003)
                nexttrainingmsg.set_author(name='Upcoming Training Sessions', icon_url=client.user.avatar_url)
                nexttrainingmsg.add_field(name='Upcoming ID Trainings', value=('\n'.join(nextIDtrainings) if len(nextIDtrainings) > 0 else '\a'), inline=False)
                nexttrainingmsg.add_field(name='Upcoming PO Trainings', value=('\n'.join(nextPOtrainings) if len(nextPOtrainings) > 0 else '\a'), inline=False)
                nexttrainingmsg.set_footer(icon_url=client.user.avatar_url, text='Nexttraining list generated at: ' + str(datetime.datetime.now() - datetime.timedelta(hours=11)))
                await message.channel.send(embed=nexttrainingmsg)
            elif messege.startswith('mytraining'):
                AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                mycursor = AltonDB.cursor(buffered=True)
                mycursor.execute("SELECT * FROM `trainingsessions` WHERE `Host` = '" + str(message.author.id) + "' ORDER BY `trainingsessions`.`TrainingTime` ASC;")
                trainingsessions = mycursor.fetchall()
                hostedtrainingsessions = []
                cohostedtrainingsessions = []
                for row in trainingsessions:
                    hostedtrainingsessions.append(row[1] + ' at ' + row[2].strftime('%d/%m/%Y at %I:%M %p'))
                mycursor.execute("SELECT * FROM `trainingsessions` WHERE `Cohost` = '" + str(message.author.id) + "' ORDER BY `trainingsessions`.`TrainingTime` ASC;")
                trainingsessions = mycursor.fetchall()
                for row in trainingsessions:
                    cohostedtrainingsessions.append(row[1] + ' at ' + row[2].strftime('%d/%m/%Y at %I:%M %p'))
                hostedtrainingmsg = discord.Embed(description='Showing hosted/co-hosted training sessions!', color=3447003)
                hostedtrainingmsg.set_author(name='Upcoming Training Sessions', icon_url=client.user.avatar_url)
                hostedtrainingmsg.add_field(name='Hosted Trainings', value=(('\n'.join(hostedtrainingsessions)) if len(hostedtrainingsessions) > 0 else '\a'), inline=False)
                hostedtrainingmsg.add_field(name='Co-hosted Trainings', value=('\n'.join(cohostedtrainingsessions) if len(cohostedtrainingsessions) > 0 else '\a'), inline=False)
                hostedtrainingmsg.set_footer(icon_url=client.user.avatar_url, text='Hosted trainings list generated at: ' + str(datetime.datetime.now() - datetime.timedelta(hours=11)))
                await message.channel.send(embed=hostedtrainingmsg)
            elif messege.startswith('warn '):
                roles = []
                for i in message.author.roles:
                    roles.append(i.name)
                print(roles)
                if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                    warning = messege.split(' ', maxsplit=2)
                    warning[1] = tagtoid(warning[1], message)
                    AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                    mycursor = AltonDB.cursor(buffered=True)
                    try:
                        mycursor.execute("INSERT INTO warnlist (Warned, Warner, Reason) VALUES ('" + warning[1] + "', '" + str(message.author.id) + "', '" + warning[2] + "');")
                        AltonDB.commit()
                        mycursor.execute("SELECT * FROM `warnlist` WHERE `Warned` = '" + warning[1] + "'")
                        noofwarns = mycursor.rowcount
                        await message.channel.send((((('<@' + warning[1]) + '> has been warned for: ') + warning[2]) + '. This is warning number ') + str(noofwarns))
                        try:
                            await message.guild.get_member(int(warning[1])).send('You have been warned from Alton County Railways for: ' + warning[2])
                        except discord.errors.Forbidden:
                            pass
                        if (noofwarns == 3) or (noofwarns == 6):
                            try:
                                await message.channel.send(((('<@' + warning[1]) + '> will now be kicked for having ') + str(noofwarns)) + ' warnings.')
                                try:
                                    await message.guild.get_member(int(warning[1])).send(('You have been kicked from Alton County Railways for having ' + str(noofwarns)) + ' warnings.')
                                except discord.errors.Forbidden:
                                    pass
                                await message.guild.kick(message.guild.get_member(int(warning[1])), reason=str(noofwarns) + ' warnings')
                            except discord.errors.Forbidden:
                                await message.channel.send("Sorry, I don't have the permissions to kick that user.")
                        elif (noofwarns > 8):
                            try:
                                await message.channel.send(((('<@' + warning[1]) + '> will now be banned for having ') + str(noofwarns)) + ' warnings.')
                                try:
                                    await message.guild.get_member(int(warning[1])).send(('You have been banned from Alton County Railways for having ' + str(noofwarns)) + ' warnings.')
                                except discord.errors.Forbidden:
                                    pass
                                await message.guild.ban(message.guild.get_member(int(warning[1])), reason=str(noofwarns) + ' warnings')
                                mycursor.execute("INSERT INTO warnlist (Banned, Banner, Reason) VALUES ('" + warning[1] + "', '" + str(message.author.id) + "', '" + str(noofwarns) + " warnings');")
                                AltonDB.commit()
                            except discord.errors.Forbidden:
                                await message.channel.send("Sorry, I don't have the permissions to ban that user.")

                    except IndexError:
                        await message.channel.send('A reason is needed to issue a warning.')
                else:
                    await message.channel.send('Sorry, you have to be an SD+ to warn.')
            elif messege.startswith('kick '):           
                roles = []
                for i in message.author.roles:
                    roles.append(i.name)
                print(roles)
                if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                    kickinfo = messege.split(' ', maxsplit=2)
                    try:
                        kickinfo[1] = tagtoid(kickinfo[1], message)
                        await message.channel.send(((('<@' + kickinfo[1]) + '> has been kicked for: ') + kickinfo[2]) + '.')
                        try:
                            await message.guild.get_member(int(kickinfo[1])).send('You have been kicked from Alton County Railways for: ' + kickinfo[2])
                        except discord.errors.Forbidden:
                            pass
                        await message.guild.kick(message.guild.get_member(int(kickinfo[1])), reason=kickinfo[2])
                    except discord.errors.Forbidden:
                        await message.channel.send('I do not have permission to kick this user.')
                    except IndexError:
                        await message.channel.send('A reason is needed to kick.')
                else:
                    await message.channel.send('Sorry, you have to be an SD+ to kick.')
            elif messege.startswith('ban '):
                roles = []
                for i in message.author.roles:
                    roles.append(i.name)
                print(roles)
                if ('Executive Team' in roles) or ('Management Team' in roles):
                    baninfo = messege.split(' ', maxsplit=2)
                    baninfo[1] = tagtoid(baninfo[1], message)
                    AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                    mycursor = AltonDB.cursor(buffered=True)
                    try:
                        await message.channel.send(((('<@' + baninfo[1]) + '> has been banned for: ') + baninfo[2]) + '.')
                        try:
                            await message.guild.get_member(int(baninfo[1])).send('You have been banned from Alton County Railways for: ' + baninfo[2])
                        except discord.errors.Forbidden:
                            pass
                        except AttributeError:
                            pass
                        await message.guild.ban(message.guild.get_member(int(baninfo[1])), reason=baninfo[2])
                        mycursor.execute("INSERT INTO banlist (Banned, Banner, Reason) VALUES ('" + baninfo[1] + "', '" + str(message.author.id) + "', '" + baninfo[2] + "');")
                        AltonDB.commit()
                    except discord.errors.Forbidden:
                        await message.channel.send('I do not have permissions to ban this user.')
                    except IndexError:
                        await message.channel.send('A reason is needed to kick.')
                else:
                    await message.channel.send('Sorry, you have to be an MOD+ to ban.')
            elif messege.startswith('warnings'):
                roles = []
                msg = []
                search = ''
                if len(messege) > 9:
                    search = " WHERE `Warned` = " + tagtoid(messege[9:], message)
                for i in message.author.roles:
                    roles.append(i.name)
                if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                    AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                    mycursor = AltonDB.cursor(buffered=True)
                    mycursor.execute("SELECT * FROM `warnlist`" + search + " ORDER BY `warnlist`.`Warned` ASC")
                    warnings  = mycursor.fetchall()
                    for row in warnings:
                        try:
                            try:
                                warned = message.guild.get_member(int(row[1])).nick
                                if warned == None:
                                    raise AttributeError()
                            except AttributeError:
                                warned = await client.get_user_info(int(row[1]))
                                warned = warned.name
                        except discord.errors.NotFound:
                            warned = str(row[1])
                        try:
                            try:
                                warner = message.guild.get_member(int(row[2])).nick
                                if warner == None:
                                    raise AttributeError()
                            except AttributeError:
                                warner = await client.get_user_info(int(row[2]))
                                warner = warner.name
                        except discord.errors.NotFound:
                            warner = str(row[2])
                        msg.append('*' + warned + '* was warned by *' + warner + '* for reason: ' + row[3])
                    try:
                        await message.channel.send('\n'.join(msg))
                    except discord.errors.HTTPException:
                        await message.channel.send('This user has no warnings.')
            elif messege.startswith('clearwarn'):
                part = message.content.split(' ')
                roles = []
                for i in message.author.roles:
                    roles.append(i.name)
                if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                    part[1] = tagtoid(part[1], message)
                    AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                    mycursor = AltonDB.cursor(buffered=True)
                    mycursor.execute("DELETE FROM `warnlist` WHERE `warned` = '" + part[1] + "'")
                    noofwarns = mycursor.rowcount
                    AltonDB.commit()
                    try:
                        nickname = message.guild.get_member(int(part[1])).nick
                    except AttributeError:
                        try:
                            nickname = await client.get_user_info(int(part[1]))
                            nickname = nickname.name
                        except discord.errors.NotFound:
                            nickname = str(part[1])
                    if nickname == None:
                        nickname = await client.get_user_info(int(part[1]))
                        nickname = nickname.name
                    await message.channel.send('Successfully cleared ' + str(noofwarns) + ' warnings for ' + nickname)
                else:
                    await message.channel.send('You have to be an SD+ to clear warnings.')
            elif messege.lower().startswith('ldappresponse'):
                await message.channel.send("Sorry, this function isn't ready just yet, please try again later!")
            elif messege.lower().startswith('help moderation'):
                HelpMsg = discord.Embed(title='Help Page', description='This is a page full of moderation commands you can use with AltonBot', color=3447003)
                HelpMsg.set_author(name='Alton Bot', icon_url=client.user.avatar_url)
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'warn [user]', value='**SD+ Only** - warns a user')
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'kick [user]', value='**SD+ Only** - kicks a user')
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'ban [user]', value='**MOD+ Only** - bans a user indefinetely or until unbanned.')
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'warnings [user(optional)]', value='Displays all warnings currently stored in memory or just for the user.')
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'clearwarnings [user]', value='**SD+ Only** - clears the warnings of a certain player.')
                HelpMsg.set_footer(icon_url=client.user.avatar_url, text='© Alton County Railways')
                await message.channel.send(embed=HelpMsg)
            elif messege.lower().startswith('help training'):
                HelpMsg = discord.Embed(title='Help Page', description='This is a page full of training commands you can use with AltonBot', color=3447003)
                HelpMsg.set_author(name='Alton Bot', icon_url=client.user.avatar_url)
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'nexttraining', value='Shows upcoming training sessions.')
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'trainingreminder [id]', value='**SD+ Only** - Sends a training reminder about the specified training.')
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'edittraining [id] [fieldtochange]: [valuetochangeto]', value='**SD+ Only** - edits training session specified **Currently in BETA**')
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'canceltraining [id]', value='**SD+ Only** - deletes training session specified.')
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'mytrainings', value='**SD+ Only** - Displays your hosted training sessions. **COMING SOON**')
                HelpMsg.set_footer(icon_url=client.user.avatar_url, text='© Alton County Railways')
                await message.channel.send(embed=HelpMsg)
            elif messege.lower().startswith('help other'):
                HelpMsg = discord.Embed(title='Help Page', description='This is a page full of other commands you can use with AltonBot', color=3447003)
                HelpMsg.set_author(name='Alton Bot', icon_url=client.user.avatar_url)
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'help', value='Displays a help page.')
                HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id)) + 'prefix', value='Changes the prefix for commands')
                HelpMsg.set_footer(icon_url=client.user.avatar_url, text='© Alton County Railways')
                await message.channel.send(embed=HelpMsg)
            elif messege.startswith('help'):
                HelpMsg = discord.Embed(title='Help Page', description='There are two types of commands you can use with AltonBot. \nPlease type ' + CMDPrefix.get(message.guild.id) + 'help [type] to see help for a certain type of command', color=3447003)
                HelpMsg.set_author(name='Alton Bot', icon_url=client.user.avatar_url)
                HelpMsg.add_field(name='Moderation', value='This includes all the commands that warn, ban and kick users.')
                HelpMsg.add_field(name='Trainings', value='This includes all the commands that the bot can do in regards to trainings')
                HelpMsg.add_field(name='Other', value='This includes any other commands that AltonBot can do')
                HelpMsg.set_footer(icon_url=client.user.avatar_url, text='© Alton County Railways')
                await message.channel.send(embed=HelpMsg)
            elif messege.startswith('prefix'):
                if len(messege) < 8:
                    await message.channel.send('Your prefix has been set to the default(!) from ' + CMDPrefix.get(message.guild.id))
                    CMDPrefix.update({
                        message.guild.id: '!',
                    })
                    with open('ServerPrefixes.py', 'w') as f:
                        f.write('CMDPrefix = {\n')
                        for (key, val) in CMDPrefix.items():
                            f.write(((("    '" + key) + "':'") + val) + "',\n")
                        f.write('}\n')
                elif len(messege) > 7:
                    await message.channel.send((('You have changed your prefix from ' + CMDPrefix.get(message.guild.id)) + ' to ') + messege[7:])
                    CMDPrefix.update({
                        message.guild.id: messege[7:],
                    })
                    with open('ServerPrefixes.py', 'w') as f:
                        f.write('CMDPrefix = {\n')
                        for (key, val) in CMDPrefix.items():
                            f.write(((("    '" + key) + "':'") + val) + "',\n")
                        f.write('}\n')
                await client.change_presence(activity=discord.Game(name=(CMDPrefix.get(514155943525875716) if 514155943525875716 in CMDPrefix else '!') + 'help'))
            elif messege.startswith('await'):
                if message.author.id == 244596682531143680:
                    await message.delete()
                    await eval(messege[6:])
                else:
                    await message.channel.send('Sorry lucky962 is the only person who can run this command at this moment.')
            elif messege.startswith('rawcommand'):
                if message.author.id == 244596682531143680:
                    exec(message[11:])
                else:
                    await message.channel.send('Sorry lucky962 is the only person who can run this command at this moment.')
            else:
                await message.channel.send("Sorry, command not found. If you believe this is an error, please dm lucky9621.")
        elif message.content.startswith('?warn') or message.content.startswith('?kick') or message.content.startswith('?ban'):
            await message.channel.send('Please use AltonBot for this operation.')
    except:
        await message.channel.send((traceback.format_exc().replace('leote','username')).split('\n')[-2])
        

@client.event
async def on_reaction_add(reaction, user):
    try:
        if reaction.emoji == '✅':
            if reaction.message.channel == client.get_channel(requestchannel):
                trainingtype = time = host = cohost = ''
                try:
                    trainingtype = re.search('Type:(.*)\n', reaction.message.content).group(1).strip('*').strip(' ')
                except:
                    try:
                        trainingtype = re.search('Type:(.*)', reaction.message.content).group(1).strip('*').strip(' ')
                    except:
                        await reaction.message.channel.send('Error finding Training Type')
                print(trainingtype)
                try:
                    time = re.search('Time:(.*)\n', reaction.message.content).group(1).strip('*').strip(' ')
                except:
                    try:
                        time = re.search('Time:(.*)', reaction.message.content).group(1).strip('*').strip(' ')
                    except:
                        await reaction.message.channel.send('Error finding Time')
                print(time)
                if 'GMT' in time:
                    formattedtime = time = re.search('Time: (.*)GMT', reaction.message.content).group(1).strip()
                else:
                    formattedtime = time = re.search('Time: (.*)', reaction.message.content).group(1).strip()
                print(formattedtime)
                try:
                    date = re.search('Date:(.*)\n', reaction.message.content).group(1).strip('*').strip(' ')
                except:
                    try:
                        date = re.search('Date:(.*)', reaction.message.content).group(1).strip('*').strip(' ')
                    except:
                        await reaction.message.channel.send('Error finding Date')
                print(date)
                if ('pm' in formattedtime.lower()) or ('am' in formattedtime.lower()):
                    formattedtime = time = formattedtime.replace(' ', '')
                    formattedtime = (date + ' ') + formattedtime
                    TrainingTime = datetime.datetime.strptime(formattedtime, '%d/%m/%Y %I:%M%p')
                    time = datetime.datetime.strptime(str(time), '%I:%M%p')
                elif (not (':' in formattedtime)):
                    if len(formattedtime) == 4:
                        formattedtime = time = (formattedtime[:2] + ':') + formattedtime[2:]
                    elif len(formattedtime) == 3:
                        formattedtime = time = (('0' + formattedtime[:1]) + ':') + formattedtime[1:]
                    formattedtime = (date + ' ') + formattedtime
                    TrainingTime = datetime.datetime.strptime(formattedtime, '%d/%m/%Y %H:%M')
                    time = datetime.datetime.strptime(str(time), '%H:%M')
                elif ':' in formattedtime:
                    formattedtime = (date + ' ') + formattedtime
                    TrainingTime = datetime.datetime.strptime(formattedtime, '%d/%m/%Y %H:%M')
                    time = datetime.datetime.strptime(str(time), '%H:%M')
                else:
                    await reaction.message.channel.send('Time Format not recognised')
                currenttime = str(datetime.datetime.now() - datetime.timedelta(hours=11))
                currenttime = datetime.datetime.strptime(currenttime, '%Y-%m-%d %H:%M:%S.%f')
                # posttime = (time - datetime.timedelta(minutes=10)).strftime('%I:%M %p')
                time = str(time.strftime('%I:%M %p'))
                # diff = relativedelta(TrainingTime, currenttime)
                try:
                    host = re.search('Host:(.*)\n', reaction.message.content).group(1).strip('*').strip(' ')
                except:
                    try:
                        host = re.search('Host:(.*)', reaction.message.content).group(1).strip('*').strip(' ')
                    except:
                        await reaction.message.channel.send('Error finding Host')
                print(host)
                try:
                    cohost = re.search('Co-host:(.*)\n', reaction.message.content).group(1).strip('*').strip(' ')
                except:
                    try:
                        cohost = re.search('Co-host:(.*)', reaction.message.content).group(1).strip('*').strip(' ')
                    except:
                        cohost == ''
                print(cohost)
                host = tagtoid(host, reaction.message)
                if host == None:
                    await reaction.message.send("Host user not found.")
                if cohost != '':
                    cohostz = tagtoid(cohost, reaction.message)
                    if cohostz != None:
                        cohost = cohostz
                        print(cohost)
                print(host)
                date = datetime.datetime.strptime(str(date), '%d/%m/%Y').strftime('%d %B %Y')
                date = str(date)
                time = time + ' GMT'
                print('tasdfad')
                if ('Dispatch' in trainingtype) or ('DS' in trainingtype) or ('Platform' in trainingtype) or ('PO' in trainingtype):
                    trainingtype = 'Platform Operator Training'
                    # notifiedrank = 'INTERMEDIATE DRIVERS'
                    # trainedrank = 'Platform Operator **[PO]**'
                elif ('Experience' in trainingtype) or ('ED' in trainingtype) or ('Intermediate' in trainingtype) or ('ID' in trainingtype):
                    trainingtype = 'Intermediate Driver Training'
                    # notifiedrank = 'NOVICE DRIVERS'
                    # trainedrank = 'Intermediate Driver **[ID]**'
                elif 'Dev' in trainingtype:
                    trainingtype = 'Developer Training'
                    # notifiedrank = 'Trainee Developer'
                    # trainedrank = 'Developer'
                else:
                    await reaction.message.channel.send('Sorry, training type not recognised, if this is a special type of training, you will have to manually make training notices, or you can notify lucky9621 to add the training type. It will be recorded in training history though.')
                if cohost == None:
                    cohosttemp = ');'
                    cohosttempz = ''
                else:
                    cohosttemp = (", '" + cohost) + "');"
                    cohosttempz = ', Cohost'
                AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
                mycursor = AltonDB.cursor(buffered=True)
                mycursor.execute((((((((((('INSERT INTO trainingsessions (ID, TrainingType, TrainingTime, Host' + cohosttempz) + ") VALUES ('") + str(reaction.message.id)) + "', '") + trainingtype) + "', '") + str(TrainingTime)) + "', '") + host) + "'") + cohosttemp)
                AltonDB.commit()
                # await client.get_channel(noticechannel).send((((((((((((((((((((('Attention **' + notifiedrank) + "**, just letting you know that there'll be a ") + trainedrank) + ' Training in **') + str(diff.days)) + ' days, ') + str(diff.hours)) + ' hours, ') + str(diff.minutes)) + ' minutes  / ') + time) + '!** (') + date) + ') \n\nHost: ') + host) + ((' \nCo-host: ' + cohost) + '\n' if cohost != None else '\n')) + '\nThe link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**') + posttime) + '**].\n\nOnce you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__\n\nThanks for reading,\n**') + reaction.message.author.nick) + '**')
                # await reaction.message.channel.send(('Thank you for hosting a Training session, please remember your id, ' + str(reaction.message.id)) + ', in order to run more commands for your training session in the future using AltonBot')
                approvedby = await reaction.users().flatten()
                await reaction.message.guild.get_member(int(host)).send('Thank you for hosting a(n) ' + trainingtype + TrainingTime.strftime(' at %I:%M%p on %d/%m/%Y') + '. Your training was approved by ' + approvedby[0].nick + '! Your id for this training is: ' + str(reaction.message.id))
    except:
        await reaction.message.channel.send((traceback.format_exc().replace('leote','username')).split('\n')[-2])

client.run(TOKEN)