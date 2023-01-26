import discord

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

class TaskAdder(commands.Cog):
  def __init__(self, CLIENT):
    self.arg1_acceptable = ['Daily', 'Weekly']
    self.arg2_acceptable = ['Easy', 'Medium', 'Hard']
    self.wrong_param = discord.Embed(title = 'Failure', description = 'Something went wrong with one of your parameters.', color = 0x02caca)
    self.wrong_param.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))
    self.wrong_param2 = discord.Embed(title = 'Failure', description = 'Something went wrong with updating the task pool.', color = 0x02caca)
    self.wrong_param2.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))
    self.weekly = discord.Embed(title = 'Success', description = 'The weekly task pool was successfully updated.', color = 0x02caca)
    self.weekly.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))
    self.daily = discord.Embed(title = 'Success', description = 'The daily task pool was successfully updated.', color = 0x02caca)
    self.daily.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))

  @commands.command()
  async def addtask(self, context, *args):
    if len(args) == 4:
      if args[1].capitalize() in self.arg1_acceptable:
        pass
        if args[2].capitalize() in self.arg2_acceptable:
          pass
          if args[3].isnumeric():
            try:
              UserData = COLLECTION.find_one({'_id': 'TaskMaster'})
              if args[1].capitalize() == 'Daily':
                Task_Pool = UserData['daily_pool']
                Task_Pool.append([args[0], args[1], args[2], args[3]])
                COLLECTION.update_one({'_id': 'TaskMaster'}, {'$set': {'daily_pool': Task_Pool}})
                await context.send(embed = self.daily)
              else:
                Task_Pool = UserData['weekly_pool']
                Task_Pool.append([args[0], args[1], args[2], args[3]])
                COLLECTION.update_one({'_id': 'TaskMaster'}, {'$set': {'weekly_pool': Task_Pool}})
                await context.send(embed = self.weekly)
            except:
              await context.send(embed = self.wrong_param2)
          else:
            await context.send(embed = self.wrong_param)
        else:
          await context.send(embed = self.wrong_param)
      else:
        await context.send(embed = self.wrong_param)
    else:
      await context.send(embed = self.wrong_param)
    
async def setup(CLIENT):
  await CLIENT.add_cog(TaskAdder(CLIENT))