import discord
import random

from datetime import datetime
from pytz import timezone
from discord.ext import commands
from pymongo import MongoClient

CLUSTER = MongoClient(
        'mongodb+srv://joelk:1234p@cluster0.xml5y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    )
DATABASE = CLUSTER['TaskMaster']
COLLECTION = DATABASE['UserData']

TIME_ZONE = timezone('EST')

BotData = COLLECTION.find_one({'_id': 'TaskMaster'})

class TaskEnroller(commands.Cog):
  def __init__(self, CLIENT):
    self.daily_drawn = []
    self.weekly_drawn = []
    self.complete = ['1', '2', '3', '4', '5']

  @commands.command()
  async def issuetasks(self, context, *args):
    UserData = COLLECTION.find_one({'_id': str(context.author.name.title())})
    daily_tasks = BotData['daily_pool']
    #weekly_tasks = Botdata['weekly_pool']
    await context.send('{}: {}'.format(daily_tasks, len(daily_tasks)))
    for i in range(len(daily_tasks)):
      r = random.randint(0,len(daily_tasks)-1)
      if r not in daily_tasks:
        daily_tasks.append(r)
        users_daily = UserData['my_daily']
        users_daily.append(BotData['daily_pool'][r])
        COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'my_daily': users_daily}})
    daily_tasks = [] 
    
  @commands.command()
  async def tm(self, context, *args):
    if len(args) > 0 and args[0] == 'complete' and args[1] in self.complete:
      UserData = COLLECTION.find_one({'_id': str(context.author.name.title())})
      task_daily = False
      task_weekly = False
      if int(args[1]) > 3:
        if UserData['my_daily'][int(args[1])-4][1] == '🟩':
          task_weekly = True
      else:
        if UserData['my_daily'][int(args[1])-1][1] == '🟩':
          task_daily = True
      
      if  task_weekly or task_daily:
        await context.send('You have already completed this task.')
      else:
        if int(args[1]) < 4:
          new_array = UserData['my_daily']
          new_array[int(args[1])-1][1] = '🟩'
          COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'my_daily': new_array}})
          complete = discord.Embed(description = 'You have completed the task: *{}*. Congratulations, you have been awarded {} points!'.format(UserData['my_daily'][int(args[1])-1][0][0].replace('_', ' '), UserData['my_daily'][int(args[1])-1][0][3]), color = 0x02caca)
          points = str(int(UserData['points']) + int(UserData['my_daily'][int(args[1])-1][0][3]))
          daily_cum = int(UserData['daily_task_completed']) + 1
          COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'points': points}})
          COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'daily_task_completed': daily_cum}})
          if UserData['my_daily'][int(args[1])-4][0][2] == 'easy':
            easy = int(UserData['easy']) + 1 
            COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'easy': easy}})
          else:
            if UserData['my_daily'][int(args[1])-4][0][2] == 'medium':
              medium = int(UserData['medium']) + 1 
              COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'medium': medium}})
            else:
              hard = int(UserData['hard']) + 1 
              COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'hard': hard}})
        else:
          if UserData['my_weekly'][int(args[1])-4][0][2] == 'easy':
            easy = int(UserData['easy']) + 1 
            COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'easy': easy}})
          else:
            if UserData['my_weekly'][int(args[1])-4][0][2] == 'medium':
              medium = int(UserData['medium']) + 1 
              COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'medium': medium}})
            else:
              hard = int(UserData['hard']) + 1 
              COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'hard': hard}})
          new_array = UserData['my_weekly']
          new_array[int(args[1])-4][1] = '🟩'
          COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'my_weekly': new_array}})
          complete = discord.Embed(description = 'You have completed the task: *{}*. Congratulations, you have been awarded {} points!'.format(UserData['my_weekly'][int(args[1])-4][0][0].replace('_', ' '), UserData['my_weekly'][int(args[1])-4][0][3]), color = 0x02caca)
          points = str(int(UserData['points']) + int(UserData['my_weekly'][int(args[1])-4][0][3]))
          weekly_cum = int(UserData['daily_task_completed']) + 1
          COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'weekly_task_completed': weekly_cum}})
          COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'points': points}})
  
        total_tasks = str((int(UserData['cumulative_task_completed'])+1))
        current_tasks = int(UserData['current_tasks']) - 1
        COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'cumulative_task_completed': total_tasks}})
        COLLECTION.update_one({'_id': str(context.author.name.title())}, {'$set': {'current_tasks': current_tasks}})
        complete.set_author(name='{} Has Completed a Task'.format(context.author.name.title()), icon_url = context.author.avatar)
        complete.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))
        await context.send(embed = complete)

      
    if len(args) > 0 and args[0] == 'tasks':
      my_tasks = discord.Embed(color = 0x02caca)
      UserData = COLLECTION.find_one({'_id': str(context.author.name.title())})
      for i, task in enumerate(UserData['my_daily']):
        my_tasks.add_field(name = '{}.) {} | Daily'.format(i+1, task[0][0].replace('_', ' ')), value = 'Points: `{}` Difficulty: `{}` Status: `{}`'.format(task[0][3], task[0][2].capitalize(), task[1]), inline = False)
      for i, task in enumerate(UserData['my_weekly']):
        my_tasks.add_field(name = '{}.) {} | Weekly'.format(i+4, task[0][0].replace('_', ' ')), value = 'Points: `{}` Difficulty: `{}` Status: `{}`'.format(task[0][3], task[0][2].capitalize(), task[1]), inline = False)
      my_tasks.set_author(name='{}\'s Tasks'.format(context.author.name.title()), icon_url = context.author.avatar)
      my_tasks.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))
      await context.send(embed = my_tasks)

      
    if len(args) > 0 and args[0] == 'enroll':
      try:
        user_daily = []
        daily_tasks = BotData['daily_pool']
        i = 0
        while i != 3:
          r = random.randint(0,len(daily_tasks)-1)
          if r not in self.daily_drawn:
            self.daily_drawn.append(r)
            u_d = [BotData['daily_pool'][r], '🟥']
            user_daily.append(u_d)
            i += 1
        self.daily_drawn = []
        user_weekly = []
        weekly_tasks = BotData['weekly_pool']
        i = 0
        while i != 2:
          r = random.randint(0,len(weekly_tasks)-1)
          if r not in self.weekly_drawn:
            self.weekly_drawn.append(r)
            u_d = [BotData['weekly_pool'][r], '🟥']
            user_weekly.append(u_d)
            i += 1
        self.weekly_drawn = []
        user = str(context.author.name.title())
        post = {
          '_id': user,
          'current_tasks': 5,
          'weekly_task_completed': 0,
          'daily_task_completed': 0,
          'cumulative_task_completed': 0,
          'overall_tasks_given': 5,
          'average_tasks_completed': 0,
          'points': 1000,
          'easy': 0,
          'medium': 0,
          'hard': 0,
          'my_daily': user_daily,
          'my_weekly': user_weekly
        }
        COLLECTION.insert_one(post)
        enrolled_users = BotData['enrolled_users']
        enrolled_users.append(str(context.author.name.title()))
        COLLECTION.update_one({'_id': 'TaskMaster'}, {'$set': {'enrolled_users': enrolled_users}})
        embed_success = discord.Embed(title = 'Success', description = 'Enrollment for user *{}* was successful and your tasks are now available, good luck!'.format(context.author.name.title()), color = 0x02caca)
        embed_success.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))
        await context.send(embed = embed_success)
      except:
        embed_failure = discord.Embed(title = 'Failure', description = 'Enrollment for user *{}* has failed. You are already enrolled, or an error has occurred.'.format(context.author.name.title()), color = 0x02caca)
        embed_failure.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))
        await context.send(embed = embed_failure)
    if len(args) > 0 and args[0] == 'stats':
      UserData = COLLECTION.find_one({'_id': str(context.author.name.title())})
      embed_stats = discord.Embed(title = '', color = 0x02caca)
      embed_stats.add_field(name = '**Points**', value = '`{}`'.format(UserData['points']), inline = True)
      embed_stats.add_field(name = '**Performance**', value = '`{}%`'.format((int(UserData['cumulative_task_completed'])/int(UserData['overall_tasks_given'])*100)), inline = True)
      embed_stats.add_field(name = '**Total Tasks Received**', value = '`{}`'.format(UserData['overall_tasks_given']), inline = True)
      embed_stats.add_field(name = '**Total Tasks Completed**', value = '`{}`'.format(UserData['cumulative_task_completed']), inline = True)
      embed_stats.add_field(name = '**Daily Tasks Completed**', value = '`{}`'.format(UserData['daily_task_completed']), inline = True)
      embed_stats.add_field(name = '**Weekly Tasks Completed**', value = '`{}`'.format(UserData['weekly_task_completed']), inline = True)
      embed_stats.add_field(name = '**Easy Tasks Completed**', value = '`{}`'.format(UserData['easy']), inline = True)
      embed_stats.add_field(name = '**Medium Tasks Completed**', value = '`{}`'.format(UserData['medium']), inline = True)
      embed_stats.add_field(name = '**Hard Tasks Completed**', value = '`{}`'.format(UserData['hard']), inline = True)
      embed_stats.set_author(name='{}\'s Stats'.format(context.author.name.title()), icon_url = context.author.avatar)
      embed_stats.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))
      embed_stats.add_field(name = '**Ongoing Tasks**', value = '`{}`'.format(UserData['current_tasks']), inline = True)
      await context.send(embed = embed_stats)
      
async def setup(CLIENT):
  await CLIENT.add_cog(TaskEnroller(CLIENT))