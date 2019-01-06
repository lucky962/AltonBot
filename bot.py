# Work with Python 3.6
import discord
import os
import re
import datetime
import mysql.connector
from dateutil.relativedelta import relativedelta
from Dependencies.ServerPrefixes import *

with open('BotToken.txt') as f:
    TOKEN = f.read()

AltonDB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Password",
    database="AltonBot"
)

noticechannel = '520701561564037143'
requestchannel = '528528451192356874'

mycursor = AltonDB.cursor()

os.chdir('Dependencies')

client = discord.Client()

@client.event
async def on_message(message):
    print(message.author)
    print(message.content)
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith(CMDPrefix.get(message.server.id) if message.server.id in CMDPrefix else '!'):
        print('COMMAND DETECTED')
        messege = message.content[len(CMDPrefix.get(message.server.id)):]
        if messege.startswith('hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)
        elif messege.startswith('trainingreminder '):
            print('TRAININGREMINDER')
            trainingid = messege[17:]
            print (trainingid)
            mycursor.execute("SELECT * FROM trainingsessions")
            for row in mycursor.fetchall():
                print(row[0])
                if str(row[0]) == trainingid:
                    print('FOUND ONE')
                    trainingtype = row[1]
                    time = str(datetime.datetime.strptime(str(row[2])[11:16], '%H:%M').strftime('%I:%M %p'))
                    date = str(datetime.datetime.strptime(str(row[2])[:10], '%Y-%m-%d').strftime('%d %B %Y'))
                    formattedtime = str(row[2])
                    host = row[3]
                    cohost = row[4]
                    TrainingTime = datetime.datetime.strptime(formattedtime, '%Y-%m-%d %H:%M:%S')
                    currenttime = str(datetime.datetime.now() - datetime.timedelta(hours=11))
                    currenttime = datetime.datetime.strptime(currenttime, '%Y-%m-%d %H:%M:%S.%f')
                    diff = relativedelta(TrainingTime, currenttime)
                    if 'Dispatch' in trainingtype or 'DS' in trainingtype or 'Platform' in trainingtype or 'PO' in trainingtype:
                        notifiedrank = 'INTERMEDIATE DRIVERS'
                        trainedrank = 'Platform Operator **[PO]**'
                    elif 'Experience' in trainingtype or 'ED' in trainingtype or 'Intermediate' in trainingtype or 'ID' in trainingtype:
                        notifiedrank = 'NOVICE DRIVERS'
                        trainedrank = 'Intermediate Driver **[ID]**'
                    print('ahsdhfadsf')
                    time = time + ' GMT'
                    await client.send_message(client.get_channel(noticechannel),"""Attention **""" + notifiedrank + """**, just a reminder that there'll be a """ + trainedrank + """ Training in **""" + str(diff.days) + """ days, """ + str(diff.hours) + """ hours, """ + str(diff.minutes) + """ minutes  / """ + time + """!** (""" + date + """) 

Host: """ + host + ((""" 
Co-host: """ + cohost + """
""") if cohost != None else '\n') + """
The link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**""" + time + """**].

Once you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__

Thanks for reading,
**""" + message.author.nick + '**')
                    await client.send_message(message.channel, 'Reminder sent!')
        elif messege.startswith('warn '):
            roles = []
            for i in message.author.roles:
                roles.append(i.name)
            print(roles)
            if 'Executive Team' in roles or 'Management Team' in roles or 'High Rank Team' in roles:
                warning = messege.split(' ', maxsplit=2)
                try:
                    if messege[5:].startswith('<@!'):
                        with open('warnlist.txt','r') as f:
                            warnings = f.readlines()
                        noofwarns = 1
                        for i in warnings:
                            parts = i.split(' ', maxsplit = 2)
                            if parts[0] == warning[1][3:len(warning[1]) - 1]:
                                noofwarns += 1
                        await client.send_message(message.channel, (warning[1] + ' has been warned for: ' + warning[2] + '. This is warning number ' + str(noofwarns)))
                        await client.send_message(message.server.get_member(warning[1][3:len(warning[1]) - 1]), 'You have been warned from Alton County Railways for: ' + warning[2])
                        if noofwarns == 3 or noofwarns == 6:
                            try:
                                await client.send_message(message.channel, (warning[1]) + ' will now be kicked for having ' + str(noofwarns) + ' warnings.')
                                await client.send_message(message.server.get_member(warning[1][3:len(warning[1]) - 1]), 'You have been kicked from Alton County Railways for having ' + str(noofwarns) + ' warnings.')
                                await client.kick(message.server.get_member(warning[1][3:len(warning[1]) - 1]))
                            except discord.errors.Forbidden:
                                await client.send_message(message.channel, 'Sorry, I don\'t have the permissions to kick that user yet.')
                        with open('warnlist.txt','r') as f:
                            warnings = f.readlines()
                        warnings.append(warning[1][3:len(warning[1]) - 1] + ' ' + message.author.id + ' ' + warning[2] + '\n')
                        with open('warnlist.txt','w') as f:
                            for i in warnings:
                                f.write(i)
                    elif messege[5:].startswith('<@'):
                        with open('warnlist.txt','r') as f:
                            warnings = f.readlines()
                        noofwarns = 1
                        for i in warnings:
                            parts = i.split(' ', maxsplit = 2)
                            if parts[0] == warning[1][2:len(warning[1]) - 1]:
                                noofwarns += 1
                        await client.send_message(message.channel, (warning[1] + ' has been warned for: ' + warning[2] + '. This is warning number ' + str(noofwarns)))
                        await client.send_message(message.server.get_member(warning[1][2:len(warning[1]) - 1]), 'You have been warned from Alton County Railways for: ' + warning[2])
                        if noofwarns == 3 or noofwarns == 6:
                            try:
                                await client.send_message(message.channel, (warning[1]) + ' will now be kicked for having ' + str(noofwarns) + ' warnings.')
                                await client.send_message(message.server.get_member(warning[1][2:len(warning[1]) - 1]), 'You have been kicked from Alton County Railways for having ' + str(noofwarns) + ' warnings.')
                                await client.kick(message.server.get_member(warning[1][2:len(warning[1]) - 1]))
                            except discord.errors.Forbidden:
                                await client.send_message(message.channel, 'Sorry, I don\'t have the permissions to kick that user yet.')
                        with open('warnlist.txt','r') as f:
                            warnings = f.readlines()
                        warnings.append(warning[1][2:len(warning[1]) - 1] + ' ' + message.author.id + ' ' + warning[2] + '\n')
                        with open('warnlist.txt','w') as f:
                            for i in warnings:
                                f.write(i)
                    else:
                        with open('warnlist.txt','r') as f:
                            warnings = f.readlines()
                        noofwarns = 1
                        for i in warnings:
                            parts = i.split(' ', maxsplit = 2)
                            if parts[0] == warning[1]:
                                noofwarns += 1
                        await client.send_message(message.channel, ('<@' + warning[1] + '> has been warned for: ' + warning[2] + '. This is warning number ' + str(noofwarns)))
                        await client.send_message(message.server.get_member(warning[1]), 'You have been warned from Alton County Railways for: ' + warning[2])
                        if noofwarns == 3 or noofwarns == 6:
                            try:
                                await client.send_message(message.channel, '<@' + warning[1] + '> will now be kicked for having ' + str(noofwarns) + ' warnings.')
                                await client.send_message(message.server.get_member(warning[1]), 'You have been kicked from Alton County Railways for having ' + str(noofwarns) + ' warnings.')
                                await client.kick(message.server.get_member(warning[1]))
                            except discord.errors.Forbidden:
                                await client.send_message(message.channel, 'Sorry, I don\'t have the permissions to kick that user yet.')
                        with open('warnlist.txt','r') as f:
                            warnings = f.readlines()
                        warnings.append(warning[1] + ' ' + message.author.id + ' ' + warning[2] + '\n')
                        with open('warnlist.txt','w') as f:
                            for i in warnings:
                                f.write(i)
                except IndexError:
                    await client.send_message(message.channel, 'A reason is needed to issue a warning.')
            else:
                await client.send_message(message.channel, ('Sorry, you have to be a part of the High Rank Team to warn.'))
        elif messege.startswith('kick '):
            print(messege[5:])
            print((messege[7:].rstrip('>')))
            print(message.author.roles)
            roles = []
            for i in message.author.roles:
                roles.append(i.name)
            print(roles)
            if 'Executive Team' in roles or 'Management Team' in roles or 'High Rank Team' in roles:
                try:
                    if messege[5:].startswith('<@!'):
                        await client.kick(message.server.get_member(messege[8:].rstrip('>')))
                    elif messege[5:].startswith('<@'):
                        await client.kick(message.server.get_member(messege[7:].rstrip('>')))
                    else:
                        await client.kick(message.server.get_member(messege[5:]))
                except discord.errors.Forbidden:
                    await client.send_message(message.channel, 'Sorry, I don\'t have the permissions to kick that user yet.')
            else:
                await client.send_message(message.channel, 'Sorry, you have to be a part of the High Rank Team to kick.')
        elif messege.startswith('warnings'):
            roles = []
            msg = []
            for i in message.author.roles:
                roles.append(i.name)
            if 'Executive Team' in roles or 'Management Team' in roles or 'High Rank Team' in roles:
                with open('warnlist.txt','r') as f:
                    warnings = f.readlines()
                for i in warnings:
                    parts = i.split(' ', maxsplit = 2)
                    print(parts)
                    msg.append('*' + str(message.server.get_member(parts[0]).nick) + '* was warned by *' + str(message.server.get_member(parts[1]).nick) + '* for reason: ' + parts[2])
                await client.send_message(message.channel, ''.join(msg))
        elif messege.startswith('clearwarnings'):
            part = message.content.split(' ')
            roles = []
            for i in message.author.roles:
                roles.append(i.name)
            if 'Executive Team' in roles or 'Management Team' in roles or 'High Rank Team' in roles:
                with open('warnlist.txt','r') as f:
                    warnings = f.readlines()
                if messege[14:].startswith('<@!'):
                    for i in warnings[:]:
                        if i.startswith(part[1][3:len(part[1]) - 1]):
                            warnings.remove(i)
                    await client.send_message(message.channel, 'Successfully cleared warnings for ' + message.server.get_member(part[1][3:len(part[1]) - 1]).name)
                elif messege[14:].startswith('<@'):
                    for i in warnings[:]:
                        if i.startswith(part[1][2:len(part[1]) - 1]):
                            warnings.remove(i)
                    await client.send_message(message.channel, 'Successfully cleared warnings for ' + message.server.get_member(part[1][2:len(part[1]) - 1]).name)
                else:
                    for i in warnings[:]:
                        if i.startswith(part[1]):
                            warnings.remove(i)
                with open('warnlist.txt','w') as f:
                    f.write(''.join(warnings))
            else:
                await client.send_message(message.channel, 'You have to be a part of the High Rank Team to clear warnings.')
        elif messege.lower().startswith('ldappresponse'):
            await client.send_message(message.channel, 'Sorry, this function isn\'t ready just yet, please try again later!')
        elif messege.startswith('help'):
            await client.send_message(message.channel, 'This command is coming soon, be ready!')
        elif messege.startswith('prefix'):
            if len(messege) < 8:
                await client.send_message(message.channel, 'Your prefix has been set to the default(!) from ' + CMDPrefix.get(message.server.id))
                CMDPrefix.update({message.server.id:'!'})
                with open('ServerPrefixes.py','w') as f:
                    f.write("CMDPrefix = {\n")
                    for key,val in CMDPrefix.items():
                        f.write('    \'' + key + '\':\'' + val + '\',\n')
                    f.write('}\n')
            elif len(messege) > 7:
                await client.send_message(message.channel, 'You have changed your prefix from ' + CMDPrefix.get(message.server.id) + ' to ' + messege[7:])
                CMDPrefix.update({message.server.id:messege[7:]})
                with open('ServerPrefixes.py','w') as f:
                    f.write("CMDPrefix = {\n")
                    for key,val in CMDPrefix.items():
                        f.write('    \'' + key + '\':\'' + val + '\',\n')
                    f.write('}\n')
        elif messege.startswith('rawcommand'):
            if message.author.id == '244596682531143680':
                exec(messege[11:])
            else: 
                await client.send_message(message.channel, 'Sorry lucky962 is the only person who can run this command at this moment.')

@client.event
async def on_reaction_add(reaction,user):
    if reaction.emoji == '✅':
        if reaction.message.channel == client.get_channel(requestchannel):
            trainingtype=time=host=cohost=notifiedrank=trainedrank=''
            try:
                trainingtype = (((re.search('Type:(.*)\n', reaction.message.content)).group(1)).strip('*')).strip(' ')
            except:
                try:
                    trainingtype = (((re.search('Type:(.*)', reaction.message.content)).group(1)).strip('*')).strip(' ')
                except:
                    await client.send_message(reaction.message.channel,'Error finding Training Type')
            print(trainingtype)
            try:
                time = (((re.search('Time:(.*)\n', reaction.message.content)).group(1)).strip('*')).strip(' ')
            except:
                try:
                    time = (((re.search('Time:(.*)', reaction.message.content)).group(1)).strip('*')).strip(' ')
                except:
                    await client.send_message(reaction.message.channel,'Error finding Time')
            print(time)
            if 'GMT' in time:
                formattedtime = time = ((re.search('Time: (.*)GMT', reaction.message.content)).group(1)).strip()
            else:
                formattedtime = time = ((re.search('Time: (.*)', reaction.message.content)).group(1)).strip()
            print(formattedtime)
            try:
                date = (((re.search('Date:(.*)\n', reaction.message.content)).group(1)).strip('*')).strip(' ')
            except:
                try:
                    date = (((re.search('Date:(.*)', reaction.message.content)).group(1)).strip('*')).strip(' ')
                except:
                    await client.send_message(reaction.message.channel,'Error finding Date')
            print(date)
            if 'pm' in formattedtime.lower() or 'am' in formattedtime.lower():
                formattedtime = time = formattedtime.replace(' ','')
                formattedtime = date + ' ' + formattedtime
                TrainingTime = datetime.datetime.strptime(formattedtime, '%d/%m/%Y %I:%M%p')
                time = str(datetime.datetime.strptime(str(time), '%I:%M%p').strftime('%I:%M %p'))
            elif not ':' in formattedtime:
                if len(formattedtime) == 4:
                    formattedtime = time = formattedtime[:2] + ':' + formattedtime[2:]
                elif len(formattedtime) == 3:
                    formattedtime = time = '0' + formattedtime[:1] + ':' + formattedtime[1:]
                formattedtime = date + ' ' + formattedtime  
                TrainingTime = datetime.datetime.strptime(formattedtime, '%d/%m/%Y %H:%M')
            elif ':' in formattedtime:
                formattedtime = date + ' ' + formattedtime
                TrainingTime = datetime.datetime.strptime(formattedtime, '%d/%m/%Y %H:%M')
                time = str(datetime.datetime.strptime(str(time), '%H:%M').strftime('%I:%M %p'))
            else:
                await client.send_message(reaction.message.channel, 'Time Format not recognised')
            currenttime = str(datetime.datetime.now() - datetime.timedelta(hours=11))
            currenttime = datetime.datetime.strptime(currenttime, '%Y-%m-%d %H:%M:%S.%f')
            diff = relativedelta(TrainingTime, currenttime)
            try:
                host = (((re.search('Host:(.*)\n', reaction.message.content)).group(1)).strip('*')).strip(' ')
            except:
                try:
                    host = (((re.search('Host:(.*)', reaction.message.content)).group(1)).strip('*')).strip(' ')
                except:
                    await client.send_message(reaction.message.channel,'Error finding Host')
            print(host)
            try:
                cohost = (((re.search('Co-host:(.*)\n', reaction.message.content)).group(1)).strip('*')).strip(' ')
            except:
                try:
                    cohost = (((re.search('Co-host:(.*)', reaction.message.content)).group(1)).strip('*')).strip(' ')
                except:
                    pass
            print(cohost)
            date = str(datetime.datetime.strptime(str(date), '%d/%m/%Y').strftime('%d %B %Y'))
            time = time + ' GMT'
            print('tasdfad')
            if 'Dispatch' in trainingtype or 'DS' in trainingtype or 'Platform' in trainingtype or 'PO' in trainingtype:
                trainingtype = 'Platform Operator Training'
                notifiedrank = 'INTERMEDIATE DRIVERS'
                trainedrank = 'Platform Operator **[PO]**'
            elif 'Experience' in trainingtype or 'ED' in trainingtype or 'Intermediate' in trainingtype or 'ID' in trainingtype:
                trainingtype = "Intermediate Driver Training"
                notifiedrank = 'NOVICE DRIVERS'
                trainedrank = 'Intermediate Driver **[ID]**'
            if cohost == None:
                cohosttemp = ');'
                cohosttempz = ''
            else:
                cohosttemp = ", '" + cohost + "');"
                cohosttempz = ", Cohost"
            mycursor.execute("INSERT INTO trainingsessions (ID, TrainingType, TrainingTime, Host" + cohosttempz + ") VALUES ('" + reaction.message.id + "', '" + trainingtype + "', '" + str(TrainingTime) + "', '" + host + "'" + cohosttemp)
            AltonDB.commit()
            await client.send_message(client.get_channel(noticechannel),"""Attention **""" + notifiedrank + """**, just letting you know that there'll be a """ + trainedrank + """ Training in **""" + str(diff.days) + """ days, """ + str(diff.hours) + """ hours, """ + str(diff.minutes) + """ minutes  / """ + time + """!** (""" + date + """) 

Host: """ + host + ((""" 
Co-host: """ + cohost + """
""") if cohost != None else '\n') + """
The link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**""" + time + """**].

Once you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__

Thanks for reading,
**""" + reaction.message.author.nick + '**')
            await client.send_message(reaction.message.channel, 'Thank you for hosting a Training session, please remember your id, ' + reaction.message.id + ', in order to run more commands for your training session in the future using AltonBot')

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='Alton County Railways'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)