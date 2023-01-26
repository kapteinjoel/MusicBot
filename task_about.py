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

class AboutTasks(commands.Cog):
  def __init__(self, CLIENT):
    self.about_page_one = discord.Embed(color = 0x02caca)
    self.about_page_one.add_field(name = 'Command | Run this command first to join', value = '`tm enroll`', inline = False)
    self.about_page_one.add_field(name = 'Command | Views the task pools', value = '`viewpool <daily or weekly>`', inline = False)
    self.about_page_one.add_field(name = 'Command | Adds a task to the pool', value = '`addtask <task_name> <daily or weekly> <easy, medium, or hard> <integer>`', inline = False)
    self.about_page_one.add_field(name = 'Command | Views your stats', value = '`tm stats`', inline = False)
    self.about_page_one.add_field(name = 'Command | Views your tasks', value = '`tm tasks`', inline = False)
    self.about_page_one.add_field(name = 'Command | Completes a desired task', value = '`tm complete <integer 1-5>`', inline = False)
    self.about_page_one.add_field(name = 'Command | Displays this message', value = '`about`', inline = False)
    self.about_page_one.set_footer(text = 'Command Prefix: \">\"')


    
    self.wrong_param = discord.Embed(title = 'Failure', description = 'Something went wrong with one of your parameters.', color = 0x02caca)
    self.wrong_param.set_footer(text = '{}'.format(datetime.now(TIME_ZONE).strftime('%I:%M %p, %m/%d/%Y')))

  @commands.command()
  async def about(self, context):
    await context.send(embed = self.about_page_one)

  @commands.command()
  async def viewpool(self, context, *args):
    if args[0].capitalize() == 'Daily':
      daily = discord.Embed(title = 'Daily Task Pool', color = 0x02caca)
      BotData = COLLECTION.find_one({'_id': 'TaskMaster'})
      for list in BotData['daily_pool']:
        daily.add_field(name = '{}'.format(list[0].capitalize().replace('_', ' ')), value = '`{}` `{}`'.format(list[2].capitalize(), list[3]), inline = False)
      await context.send(embed = daily)
    else:
      if args[0].capitalize() == 'Weekly':
        daily = discord.Embed(title = 'Weekly Task Pool', color = 0x02caca)
        BotData = COLLECTION.find_one({'_id': 'TaskMaster'})
        for list in BotData['weekly_pool']:
          daily.add_field(name = '{}'.format(list[0].capitalize().replace('_', ' ')), value = '`{}` `{}`'.format(list[2].capitalize(), list[3]), inline = False)
        await context.send(embed = daily)
      else:
        await context.send(embed = self.wrong_param)
        
async def setup(CLIENT):
  await CLIENT.add_cog(AboutTasks(CLIENT))
  
    