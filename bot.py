# Work with Python 3.6
import discord
import os
import re
import datetime
from dateutil.relativedelta import relativedelta
from Dependencies.ServerPrefixes import *

with open('BotToken.txt') as f:
    TOKEN = f.read()

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
        messege = message.content[len(CMDPrefix.get(message.server.id)):]
        if messege.startswith('hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)
        elif messege.startswith('warn '):
            roles = []
            for i in message.author.roles:
                roles.append(i.name)
            print(roles)
            if 'High Rank Team' in roles:
                warning = messege.split(' ', maxsplit=2)
                if messege[5:].startswith('<@'):
                    await client.send_message(message.channel, (warning[1] + ' has been warned for: ' + warning[2]))
                    await client.send_message(message.server.get_member(warning[1][2:len(warning[1]) - 1]), 'You have been warned from Alton County Railways for: ' + warning[2])
                    with open('warnlist.txt','r') as f:
                        warnings = f.readlines()
                    warnings.append(warning[1][2:len(warning[1]) - 1] + ' ' + message.author.id + ' ' + warning[2] + '\n')
                    with open('warnlist.txt','w') as f:
                        for i in warnings:
                            f.write(i)
                else:
                    await client.send_message(message.channel, ('<@' + warning[1] + '> has been warned for: ' + warning[2]))
                    await client.send_message(message.server.get_member(warning[1]), 'You have been warned from Alton County Railways for: ' + warning[2])
                    with open('warnlist.txt','r') as f:
                        warnings = f.readlines()
                    warnings.append(warning[1] + ' ' + message.author.id + ' ' + warning[2] + '\n')
                    with open('warnlist.txt','w') as f:
                        for i in warnings:
                            f.write(i)
            else:
                await client.send_message(message.channel, ('Sorry, you have to be a part of the High Rank Team to warn.'))
        elif messege.startswith('kick'):
            print(messege[5:])
            print((messege[7:].rstrip('>')))
            print(message.author.roles)
            roles = []
            for i in message.author.roles:
                roles.append(i.name)
            print(roles)
            if 'High Rank Team' in roles:
                try:
                    if messege[5:].startswith('<@'):
                        await client.kick(message.server.get_member(messege[7:].rstrip('>')))
                    else:
                        await client.kick(message.server.get_member(messege[5:]))
                except discord.errors.Forbidden:
                    await client.send_message(message.channel, 'Sorry, I don\'t have the permissions to kick yet.')
            else:
                await client.send_message(message.channel, 'Sorry, you have to be a part of the High Rank Team to kick.')
        elif messege.startswith('warnings'):
            roles = []
            msg = []
            for i in message.author.roles:
                roles.append(i.name)
            if 'High Rank Team' in roles:
                with open('warnlist.txt','r') as f:
                    warnings = f.readlines()
                for i in warnings:
                    parts = i.split(' ', maxsplit = 2)
                    print(parts)
                    msg.append('*' + str(message.server.get_member(parts[0]).name) + '* was warned by *' + str(message.server.get_member(parts[1]).name) + '* for reason: ' + parts[2])
                await client.send_message(message.channel, ''.join(msg))
        elif messege.startswith('clearwarnings'):
            part = message.content.split(' ')
            roles = []
            for i in message.author.roles:
                roles.append(i.name)
            if 'High Rank Team' in roles:
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

@client.event
async def on_reaction_add(reaction,user):
    if reaction.emoji == '✅':
        if reaction.message.channel == client.get_channel('528528451192356874'):
            trainingtype=time=host=cohost=notifiedrank=trainedrank=''
            try:
                trainingtype = ((re.search('Type: (.*)\n', reaction.message.content)).group(1)).strip('*')
            except:
                try:
                    trainingtype = ((re.search('Type: (.*)', reaction.message.content)).group(1)).strip('*')
                except:
                    await client.send_message(reaction.message.channel,'Error finding Training Type')
            print(trainingtype)
            try:
                time = ((re.search('Time: (.*)\n', reaction.message.content)).group(1)).strip('*')
            except:
                try:
                    time = ((re.search('Time: (.*)', reaction.message.content)).group(1)).strip('*')
                except:
                    await client.send_message(reaction.message.channel,'Error finding Time')
            print(time)
            if 'GMT' in time:
                formattedtime = ((re.search('Time: (.*)GMT', reaction.message.content)).group(1)).strip()
            else:
                formattedtime = ((re.search('Time: (.*)', reaction.message.content)).group(1)).strip()
            print(formattedtime)
            try:
                date = ((re.search('Date: (.*)\n', reaction.message.content)).group(1)).strip('*')
            except:
                try:
                    date = ((re.search('Date: (.*)', reaction.message.content)).group(1)).strip('*')
                except:
                    await client.send_message(reaction.message.channel,'Error finding Date')
            print(date)
            if 'pm' in formattedtime.lower() or 'am' in formattedtime.lower():
                formattedtime = formattedtime.replace(' ','')
                formattedtime = date + ' ' + formattedtime
                TrainingTime = datetime.datetime.strptime(formattedtime, '%d/%m/%Y %H:%M%p')
            elif not ':' in formattedtime:
                if len(formattedtime) == 4:
                    formattedtime = formattedtime[:2] + ':' + formattedtime[2:]
                elif len(formattedtime) == 3:
                    formattedtime = '0' + formattedtime[:1] + ':' + formattedtime[1:]
                formattedtime = date + ' ' + formattedtime  
                TrainingTime = datetime.datetime.strptime(formattedtime, '%d/%m/%Y %H%M')
            elif ':' in formattedtime:
                formattedtime = date + ' ' + formattedtime
                TrainingTime = datetime.datetime.strptime(formattedtime, '%d/%m/%Y %H:%M')
            else:
                await client.send_message(reaction.message.channel, 'Time Format not recognised')
            currenttime = str(datetime.datetime.now() - datetime.timedelta(hours=11))
            currenttime = datetime.datetime.strptime(currenttime, '%Y-%m-%d %H:%M:%S.%f')
            diff = relativedelta(TrainingTime, currenttime)
            try:
                host = ((re.search('Host: (.*)\n', reaction.message.content)).group(1)).strip('*')
            except:
                try:
                    host = ((re.search('Host: (.*)', reaction.message.content)).group(1)).strip('*')
                except:
                    await client.send_message(reaction.message.channel,'Error finding Host')
            print(host)
            try:
                cohost = ((re.search('Co-host: (.*)\n', reaction.message.content)).group(1)).strip('*')
            except:
                try:
                    cohost = ((re.search('Co-host: (.*)', reaction.message.content)).group(1)).strip('*')
                except:
                    pass
            print(cohost)
            print('tasdfad')
            if 'Dispatch' in trainingtype:
                notifiedrank = 'EXPERIENCED DRIVERS'
                trainedrank = 'Dispatcher **[DS]**'
            elif 'Experience' in trainingtype:
                notifiedrank = 'NOVICE DRIVERS'
                trainedrank = 'Experienced Driver **[ED]**'
            await client.send_message(client.get_channel('520701561564037143'),"""Attention **""" + notifiedrank + """**, just letting you know that there'll be a """ + trainedrank + """ Training in """ + str(diff.days) + """ days, """ + str(diff.hours) + """ hours, """ + str(diff.minutes) + """ minutes  / """ + time + """! (""" + date + """) 

Host: """ + host + ((""" 
Co-host: """ + cohost + """
""") if cohost != None else '') + """
The link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**""" + time + """**].

Once you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__

Thanks for reading,
**""" + reaction.message.author.name + '**')
        # 'asdf=5;iwantthis123jasd'
        # result = re.search('asdf=5;(.*)123jasd', s)
        # print result.group(1)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)