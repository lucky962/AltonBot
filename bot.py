import discord
import os
import re
import datetime
import mysql.connector
import time
import asyncio
from dateutil.relativedelta import relativedelta
from Dependencies.ServerPrefixes import *
print(CMDPrefix)
with open('BotToken.txt') as f:
    TOKEN = f.read()
AltonDB = mysql.connector.connect(host='localhost', user='root', passwd='Password', database='AltonBot')
noticechannel = 520701561564037143
requestchannel = 528528451192356874
mycursor = AltonDB.cursor()
os.chdir('Dependencies')
client = discord.Client()

@client.event
async def on_message(message):
    print(message.author)
    print(message.content)
    if message.author == client.user:
        return
    if message.content.startswith(CMDPrefix.get(message.guild.id) if message.guild.id in CMDPrefix else '!'):
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
                        host = row[3]
                        cohost = row[4]
                        TrainingTime = datetime.datetime.strptime(formattedtime, '%Y-%m-%d %H:%M:%S')
                        currenttime = str(datetime.datetime.now() - datetime.timedelta(hours=11))
                        currenttime = datetime.datetime.strptime(currenttime, '%Y-%m-%d %H:%M:%S.%f')
                        diff = relativedelta(TrainingTime, currenttime)
                        if ('Dispatch' in trainingtype) or ('DS' in trainingtype) or ('Platform' in trainingtype) or ('PO' in trainingtype):
                            print(trainingtype)
                            notifiedrank = 'INTERMEDIATE DRIVERS'
                            trainedrank = 'Platform Operator **[PO]**'
                        elif ('Experience' in trainingtype) or ('ED' in trainingtype) or ('Intermediate' in trainingtype) or ('ID' in trainingtype):
                            print(trainingtype)
                            notifiedrank = 'NOVICE DRIVERS'
                            trainedrank = 'Intermediate Driver **[ID]**'
                        elif 'Dev' in trainingtype:
                            print(trainingtype)
                            trainingtype = 'Developer Training'
                            notifiedrank = 'Trainee Developer'
                            trainedrank = 'Developer'
                        else:
                            await message.channel.send('Sorry, your trainingtype is not found. Please tell @lucky962#0599, if you would like him to add a new trainingytpe.')
                        print('ahsdhfadsf')
                        time = time + ' GMT'
                        await client.get_channel(noticechannel).send((((((((((((((((((((('Attention **' + notifiedrank) + "**, just a reminder that there'll be a ") + trainedrank) + ' Training in **') + str(diff.days)) + ' days, ') + str(diff.hours)) + ' hours, ') + str(diff.minutes)) + ' minutes  / ') + time) + '!** (') + date) + ') \n\nHost: ') + host) + ((' \nCo-host: ' + cohost) + '\n' if cohost != None else '\n')) + '\nThe link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**') + posttime) + '**].\n\nOnce you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__\n\nThanks for reading,\n**') + message.author.nick) + '**')
                        await message.channel.send('Reminder sent!')
        elif messege.startswith('warn '):
            roles = []
            for i in message.author.roles:
                roles.append(i.name)
            print(roles)
            if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                warning = messege.split(' ', maxsplit=2)
                try:
                    if messege[5:].startswith('<@!'):
                        with open('warnlist.txt', 'r') as f:
                            warnings = f.readlines()
                        noofwarns = 1
                        for i in warnings:
                            parts = i.split(' ', maxsplit=2)
                            print(parts[0])
                            print(warning[1][3:len(warning[1]) - 1])
                            if parts[0] == warning[1][3:len(warning[1]) - 1]:
                                noofwarns += 1
                        await message.channel.send((((warning[1] + ' has been warned for: ') + warning[2]) + '. This is warning number ') + str(noofwarns))
                        await client.get_user(int(warning[1][3:len(warning[1]) - 1])).send('You have been warned from Alton County Railways for: ' + warning[2])
                        if (noofwarns == 3) or (noofwarns == 6):
                            try:
                                await message.channel.send(((warning[1] + ' will now be kicked for having ') + str(noofwarns)) + ' warnings.')
                                await client.get_user(int(warning[1][3:len(warning[1]) - 1])).send(('You have been kicked from Alton County Railways for having ' + str(noofwarns)) + ' warnings.')
                                await message.guild.kick(client.get_user(int(warning[1][3:len(warning[1]) - 1])), reason=str(noofwarns) + 'warnings')
                            except discord.errors.Forbidden:
                                await message.channel.send("Sorry, I don't have the permissions to kick that user yet.")
                        with open('warnlist.txt', 'r') as f:
                            warnings = f.readlines()
                        warnings.append(((((warning[1][3:len(warning[1]) - 1] + ' ') + str(message.author.id)) + ' ') + warning[2]) + '\n')
                        with open('warnlist.txt', 'w') as f:
                            for i in warnings:
                                f.write(i)
                    elif messege[5:].startswith('<@'):
                        with open('warnlist.txt', 'r') as f:
                            warnings = f.readlines()
                        noofwarns = 1
                        for i in warnings:
                            parts = i.split(' ', maxsplit=2)
                            if parts[0] == warning[1][2:len(warning[1]) - 1]:
                                noofwarns += 1
                        await message.channel.send((((warning[1] + ' has been warned for: ') + warning[2]) + '. This is warning number ') + str(noofwarns))
                        await client.get_user(int(warning[1][2:len(warning[1]) - 1])).send('You have been warned from Alton County Railways for: ' + warning[2])
                        if (noofwarns == 3) or (noofwarns == 6):
                            try:
                                await message.channel.send(((warning[1] + ' will now be kicked for having ') + str(noofwarns)) + ' warnings.')
                                await client.get_user(int(warning[1][2:len(warning[1]) - 1])).send(('You have been kicked from Alton County Railways for having ' + str(noofwarns)) + ' warnings.')
                                await message.guild.kick(client.get_user(int(warning[1][2:len(warning[1]) - 1])), reason=str(noofwarns) + 'warnings')
                            except discord.errors.Forbidden:
                                await message.channel.send("Sorry, I don't have the permissions to kick that user yet.")
                        with open('warnlist.txt', 'r') as f:
                            warnings = f.readlines()
                        warnings.append(((((warning[1][2:len(warning[1]) - 1] + ' ') + str(message.author.id)) + ' ') + warning[2]) + '\n')
                        with open('warnlist.txt', 'w') as f:
                            for i in warnings:
                                f.write(i)
                    else:
                        with open('warnlist.txt', 'r') as f:
                            warnings = f.readlines()
                        noofwarns = 1
                        for i in warnings:
                            parts = i.split(' ', maxsplit=2)
                            if parts[0] == warning[1]:
                                noofwarns += 1
                        await message.channel.send((((('<@' + warning[1]) + '> has been warned for: ') + warning[2]) + '. This is warning number ') + str(noofwarns))
                        await client.get_user(int(warning[1])).send('You have been warned from Alton County Railways for: ' + warning[2])
                        if (noofwarns == 3) or (noofwarns == 6):
                            try:
                                await message.channel.send(((('<@' + warning[1]) + '> will now be kicked for having ') + str(noofwarns)) + ' warnings.')
                                await client.get_user(int(warning[1])).send(('You have been kicked from Alton County Railways for having ' + str(noofwarns)) + ' warnings.')
                                await message.guild.kick(client.get_user(int(warning[1])), reason=str(noofwarns) + 'warnings')
                            except discord.errors.Forbidden:
                                await message.channel.send("Sorry, I don't have the permissions to kick that user yet.")
                        with open('warnlist.txt', 'r') as f:
                            warnings = f.readlines()
                        warnings.append(((((warning[1] + ' ') + str(message.author.id)) + ' ') + warning[2]) + '\n')
                        with open('warnlist.txt', 'w') as f:
                            for i in warnings:
                                f.write(i)
                except IndexError:
                    await message.channel.send('A reason is needed to issue a warning.')
            else:
                await message.channel.send('Sorry, you have to be an LD+ to warn.')
        elif messege.startswith('kick '):
            print(messege[5:])
            print(messege[7:].rstrip('>'))
            print(message.author.roles)
            roles = []
            for i in message.author.roles:
                roles.append(i.name)
            print(roles)
            if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                try:
                    if messege[5:].startswith('<@!'):
                        await client.get_user(int(messege[8:].rstrip('>'))).kick()
                    elif messege[5:].startswith('<@'):
                        await client.get_user(int(messege[7:].rstrip('>'))).kick()
                    else:
                        await client.get_user(int(messege[5:])).kick() 
                except discord.errors.Forbidden:
                    await message.channel.send("Sorry, I don't have the permissions to kick that user yet.")
            else:
                await message.channel.send('Sorry, you have to be an LD+ to kick.')
        elif messege.startswith('warnings'):
            roles = []
            msg = []
            for i in message.author.roles:
                roles.append(i.name)
            if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                with open('warnlist.txt', 'r') as f:
                    warnings = f.readlines()
                for i in warnings:
                    parts = i.split(' ', maxsplit=2)
                    print(parts)
                    try:
                        msg.append((((('*' + str(client.get_user(int(parts[0])).nick)) + '* was warned by *') + str(client.get_user(int(parts[1])).nick)) + '* for reason: ') + parts[2])
                    except AttributeError:
                        try:
                            msg.append('*' + parts[0] + '* was warned by *' + str(client.get_user(int(parts[1])).nick) + '* for reason: ' + parts[2])
                        except AttributeError:
                            try:
                                msg.append('*' + str(client.get_user(int(parts[0])).nick) + '* was warned by *' + parts[1] + '* for reason: ' + parts[2])
                            except AttributeError:
                                msg.append('*' + parts[0] + '* was warned by *' + parts[1] + '* for reason: ' + parts[2])
                await message.channel.send(''.join(msg))
        elif messege.startswith('clearwarnings'):
            part = message.content.split(' ')
            roles = []
            for i in message.author.roles:
                roles.append(i.name)
            if ('Executive Team' in roles) or ('Management Team' in roles) or ('High Rank Team' in roles):
                with open('warnlist.txt', 'r') as f:
                    warnings = f.readlines()
                if messege[14:].startswith('<@!'):
                    for i in warnings[:]:
                        if i.startswith(part[1][3:len(part[1]) - 1]):
                            warnings.remove(i)
                    await message.channel.send('Successfully cleared warnings for ' + client.get_user(int(part[1][3:len(part[1]) - 1])).nick)
                elif messege[14:].startswith('<@'):
                    for i in warnings[:]:
                        if i.startswith(part[1][2:len(part[1]) - 1]):
                            warnings.remove(i)
                    await message.channel.send('Successfully cleared warnings for ' + client.get_user(int(part[1][2:len(part[1]) - 1])).nick)
                else:
                    for i in warnings[:]:
                        if i.startswithint(part[1]):
                            warnings.remove(i)
                with open('warnlist.txt', 'w') as f:
                    f.write(''.join(warnings))
            else:
                await message.channel.send('You have to be an LD+ to clear warnings.')
        elif messege.lower().startswith('ldappresponse'):
            await message.channel.send("Sorry, this function isn't ready just yet, please try again later!")
        elif messege.startswith('help'):
            HelpMsg = discord.Embed(title='Help Page', description='This is a page full of commands you can use with AltonBot', color=3447003)
            HelpMsg.set_author(name='Insults Bot', icon_url=client.user.avatar_url)
            HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id) if message.guild.id in CMDPrefix else '!') + 'help', value='Displays this help page.')
            HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id) if message.guild.id in CMDPrefix else '!') + 'trainingreminder [id]', value='**LD+ Only** - Sends a training reminder about the specified training.')
            HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id) if message.guild.id in CMDPrefix else '!') + 'warn [user]', value='**LD+ Only** - warns a user')
            HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id) if message.guild.id in CMDPrefix else '!') + 'kick [user]', value='**LD+ Only** - kicks a user')
            HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id) if message.guild.id in CMDPrefix else '!') + 'ban [user] [time]', value='**MOD+ Only** - bans a user indefinetely or for a certain time. **COMING SOON**')
            HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id) if message.guild.id in CMDPrefix else '!') + 'warnings', value='Displays all warnings currently stored in memory.')
            HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id) if message.guild.id in CMDPrefix else '!') + 'clearwarnings [user]', value='**LD+ Only** - clears the warnings of a certain player.')
            HelpMsg.add_field(name=(CMDPrefix.get(message.guild.id) if message.guild.id in CMDPrefix else '!') + 'prefix', value='Changes the prefix for commands')
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
        elif messege.startswith('rawcommand'):
            if message.author.id == 244596682531143680:
                exec(messege[11:], globals(), locals())
            else:
                await message.channel.send('Sorry lucky962 is the only person who can run this command at this moment.')

@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == '✅':
        if reaction.message.channel == client.get_channel(requestchannel):
            trainingtype = time = host = cohost = notifiedrank = trainedrank = ''
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
            posttime = (time - datetime.timedelta(minutes=10)).strftime('%I:%M %p')
            time = str(time.strftime('%I:%M %p'))
            diff = relativedelta(TrainingTime, currenttime)
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
                    pass
            print(cohost)
            date = datetime.datetime.strptime(str(date), '%d/%m/%Y').strftime('%d %B %Y')
            date = str(date)
            time = time + ' GMT'
            print('tasdfad')
            if ('Dispatch' in trainingtype) or ('DS' in trainingtype) or ('Platform' in trainingtype) or ('PO' in trainingtype):
                trainingtype = 'Platform Operator Training'
                notifiedrank = 'INTERMEDIATE DRIVERS'
                trainedrank = 'Platform Operator **[PO]**'
            elif ('Experience' in trainingtype) or ('ED' in trainingtype) or ('Intermediate' in trainingtype) or ('ID' in trainingtype):
                trainingtype = 'Intermediate Driver Training'
                notifiedrank = 'NOVICE DRIVERS'
                trainedrank = 'Intermediate Driver **[ID]**'
            elif 'Dev' in trainingtype:
                trainingtype = 'Developer Training'
                notifiedrank = 'Trainee Developer'
                trainedrank = 'Developer'
            if cohost == None:
                cohosttemp = ');'
                cohosttempz = ''
            else:
                cohosttemp = (", '" + cohost) + "');"
                cohosttempz = ', Cohost'
            mycursor.execute((((((((((('INSERT INTO trainingsessions (ID, TrainingType, TrainingTime, Host' + cohosttempz) + ") VALUES ('") + reaction.message.id) + "', '") + trainingtype) + "', '") + str(TrainingTime)) + "', '") + host) + "'") + cohosttemp)
            AltonDB.commit()
            await client.get_channel(noticechannel).send((((((((((((((((((((('Attention **' + notifiedrank) + "**, just letting you know that there'll be a ") + trainedrank) + ' Training in **') + str(diff.days)) + ' days, ') + str(diff.hours)) + ' hours, ') + str(diff.minutes)) + ' minutes  / ') + time) + '!** (') + date) + ') \n\nHost: ') + host) + ((' \nCo-host: ' + cohost) + '\n' if cohost != None else '\n')) + '\nThe link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**') + posttime) + '**].\n\nOnce you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__\n\nThanks for reading,\n**') + reaction.message.author.nick) + '**')
            await reaction.message.channel.send(('Thank you for hosting a Training session, please remember your id, ' + reaction.message.id) + ', in order to run more commands for your training session in the future using AltonBot')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=(CMDPrefix.get(514155943525875716) if 514155943525875716 in CMDPrefix else '!') + 'help'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run(TOKEN)