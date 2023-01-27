import music
import asyncio
import random

from pymongo import MongoClient
from datetime import datetime, timedelta
from threading import Thread
from pytz import timezone
from settings import *

CLUSTER = MongoClient(
        'mongodb+srv://joelk:1234p@cluster0.xml5y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    )
DATABASE = CLUSTER['TaskMaster']
COLLECTION = DATABASE['UserData']

TIME_ZONE = timezone('EST')

BOT_DATA = COLLECTION.find_one({'_id': 'TaskMaster'})


if __name__ == '__main__':
  def update_pool():
    activated = False
    activated2 = False
    while True:
      BOT_DATA = COLLECTION.find_one({'_id': 'TaskMaster'})
      if datetime.now(TIME_ZONE).strftime('%I%M%S%p') == '120000AM' and activated == False:
        print('new day')
        minus_points = 0
        activated = True
        daily_drawn = []
        user_daily = []
        daily_tasks = BOT_DATA['daily_pool']
        i = 0
        for user in BOT_DATA['enrolled_users']:
          UserData = COLLECTION.find_one({'_id': user})
          for array in UserData['my_daily']:
            if array[1] == '🟥':
              minus_points += int(array[0][3])
          points = int(UserData['points']) - minus_points
          COLLECTION.update_one({'_id': user}, {'$set': {'points': points}})   
          while i != 3:
            r = random.randint(0,len(daily_tasks)-1)
            if r not in daily_drawn:
              daily_drawn.append(r)
              u_d = [BOT_DATA['daily_pool'][r], '🟥']
              user_daily.append(u_d)
              i += 1
          COLLECTION.update_one({'_id': user}, {'$set': {'my_daily': user_daily}})
        daily_drawn = []
        
      if datetime.now().weekday() == 0 and datetime.now(TIME_ZONE).strftime('%I%M%S%p') == '120000AM' and activated2 == False:
        print('new week')
        minus_points = 0
        activated2 = True
        weekly_drawn = []
        user_weekly = []
        weekly_tasks = BOT_DATA['weekly_pool']
        i = 0
        for user in BOT_DATA['enrolled_users']:
          UserData = COLLECTION.find_one({'_id': user})
          for array in UserData['my_weekly']:
            if array[1] == '🟥':
              minus_points += int(array[0][3])
          points = int(UserData['points']) - minus_points
          COLLECTION.update_one({'_id': user}, {'$set': {'points': points}})   
          while i != 2:
            r = random.randint(0,len(weekly_tasks)-1)
            if r not in weekly_drawn:
              weekly_drawn.append(r)
              u_d = [BOT_DATA['weekly_pool'][r], '🟥']
              user_weekly.append(u_d)
              i += 1
          COLLECTION.update_one({'_id': user}, {'$set': {'my_weekly': user_weekly}})
        weekly_drawn = []

      if datetime.now(TIME_ZONE).strftime('%I%M%S%p') == '120001AM':
        activated = False
        activated2 = False

  async def add_classes():
    for i in range(len(CLASSES)):
      await CLASSES[i].setup(CLIENT)

  @CLIENT.event
  async def on_ready():
    await add_classes()
    update = Thread(target = update_pool)
    update.start()
    print("I'm online")

  @CLIENT.event
  async def on_voice_state_update(member, before, after):
    if member.guild.voice_client is not None and len(member.guild.voice_client.channel.members) == 1:
        music.Music.song_queue = []
        music.Music.audio_info = []
        await member.guild.voice_client.disconnect()

CLIENT.run(TOKEN)
