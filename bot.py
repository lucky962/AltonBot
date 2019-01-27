import discord
import os
import sys
import re
import datetime
import mysql.connector
import time
import asyncio
import traceback
from dateutil.relativedelta import relativedelta
from Dependencies.ServerPrefixes import *
from discord.ext import commands
print(CMDPrefix)
with open('BotToken.txt') as f:
    TOKEN = f.read()
hostip = '192.168.0.100'
AltonDB = mysql.connector.connect(host=hostip, user='root', passwd='Password', database='AltonBot')
noticechannel = 520701561564037143
requestchannel = 528528451192356874
guildid = 514155943525875716
mycursor = AltonDB.cursor(buffered=True)
os.chdir('Dependencies')
bot = commands.Bot(command_prefix='-')
bot.hostip = hostip
bot.noticechannel = noticechannel
bot.requestchannel = requestchannel

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
bot.tagtoid = tagtoid

async def my_background_task():
    print('automaticreminder task started')
    await bot.wait_until_ready()
    print('bot is ready')
    guild = bot.get_guild(guildid)
    gameplaying = 0
    while not bot.is_closed():
        if gameplaying == 0:
            await bot.change_presence(activity=discord.Game(name='Alton County Railways'))
            gameplaying = 1
        elif gameplaying == 1:
            await bot.change_presence(activity=discord.Game(name=(CMDPrefix.get(514155943525875716) if 514155943525875716 in CMDPrefix else '!') + 'help'))
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
                    host = await bot.get_user_info(int(row[3]))
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
                            cohost = await bot.get_user_info(int(row[4]))
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
            await bot.get_channel(noticechannel).send('Attention **' + notifiedrank + "**, just a reminder that there'll be a " + trainedrank + ' Training in **' + str(diff.days) + ' days, ' + str(diff.hours) + ' hours, ' + str(diff.minutes) + ' minutes  / ' + time + '!** (' + date + ') \n\nHost: ' + host + ' \nCo-host: ' + ((cohost + '\n') if cohost != '' else '\n') + '\nThe link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**' + posttime + '**].\n\nOnce you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__\n\nThanks for reading,\n**' + host + '**')
            mycursor.execute("UPDATE `trainingsessions` SET `Reminded` = '1' WHERE `trainingsessions`.`ID` = " + str(row[0]) + ";")
            AltonDB.commit()
            print('done')
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=(CMDPrefix.get(514155943525875716) if 514155943525875716 in CMDPrefix else '!') + 'help'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    print(message.author)
    print(message.content)
    if message.content.startswith('?warn') or message.content.startswith('?kick') or message.content.startswith('?ban'):
        await message.channel.send('You should use AltonBot for this operation. ;)')
    await bot.process_commands(message)
         

@bot.event
async def on_reaction_add(reaction, user):
    try:
        if reaction.emoji == '✅':
            if reaction.message.channel == bot.get_channel(requestchannel):
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
                # await bot.get_channel(noticechannel).send((((((((((((((((((((('Attention **' + notifiedrank) + "**, just letting you know that there'll be a ") + trainedrank) + ' Training in **') + str(diff.days)) + ' days, ') + str(diff.hours)) + ' hours, ') + str(diff.minutes)) + ' minutes  / ') + time) + '!** (') + date) + ') \n\nHost: ') + host) + ((' \nCo-host: ' + cohost) + '\n' if cohost != None else '\n')) + '\nThe link will be posted on the __**Group Wall or Group Shout (One Of the two)**__ **10** minutes before its scheduled time. [**') + posttime) + '**].\n\nOnce you join, please spawn as a __**passenger**__ at __**Standen Station**__ and line up __**against the ticket machines!**__\n\nThanks for reading,\n**') + reaction.message.author.nick) + '**')
                # await reaction.message.channel.send(('Thank you for hosting a Training session, please remember your id, ' + str(reaction.message.id)) + ', in order to run more commands for your training session in the future using AltonBot')
                approvedby = await reaction.users().flatten()
                await reaction.message.guild.get_member(int(host)).send('Thank you for hosting a(n) ' + trainingtype + TrainingTime.strftime(' at %I:%M%p on %d/%m/%Y') + '. Your training was approved by ' + approvedby[0].nick + '! Your id for this training is: ' + str(reaction.message.id))
    except:
        await reaction.message.channel.send((traceback.format_exc().replace('leote','username')).split('\n')[-2])

# I'm thinking of migrating to use the commands extension nearly everything below this should be parts of the code that have been migrated

initial_extensions = ['cogs.error_handler',
                      'cogs.training_commands',
                      'cogs.moderation_commands',
                      'cogs.other_commands']

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            traceback.print_exc()

@bot.command(name='hello', hidden=True)
async def do_canceltraining(ctx):
    msg = 'Hello {0.author.mention}'.format(ctx)
    await ctx.channel.send(msg)

@commands.command(name='setprefix')
@commands.has_any_role('Executive Team','Management Team','High Rank Team')
async def do_setprefix(ctx):
    ctx.send('Setprefix command under maintenance, will be back soon! :)')

bot.loop.create_task(my_background_task())
bot.run(TOKEN)