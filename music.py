import discord, asyncio, time

from settings import*
from threading import Thread
from discord.ext import commands
from youtube_dl import YoutubeDL
from requests import get

YDL_OPTIONS = {'format' : 'bestaudio', 'noplaylist' : 'True'}
FFMPEG_OPTIONS = {'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn'}

class Music(commands.Cog):
  def __init__(self, CLIENT):
    self.song_queue = []
    self.audio_info = []
    self.data = None
    self.audio = None
    self.context = None
    self.is_playing = False
    
    self.update_queue = Thread(target = self.try_next_song)
    self.update_queue.start()

  def try_next_song(self):
    while True:
      time.sleep(.5)
      if len(self.song_queue) >= 1:
        try:
          if not self.context.voice_client.is_playing():
            try:
              self.context.voice_client.play(self.song_queue[0], after = lambda e: asyncio.run_coroutine_threadsafe(self.context.send(embed = self.now_playing()), CLIENT.loop))
              self.song_queue.pop(0)
              self.audio_info.pop(0)
            except:
              pass
        except:
          pass

  def now_playing(self):
    if len(self.audio_info) >= 1:
      embed = discord.Embed(title = '**Now Playing | {}**'.format(self.audio_info[0][0]), description = 'Added by {} | Position {} of {}'.format(self.audio_info[0][2], 1, len(self.song_queue)), color = 0x000000)
      embed.set_thumbnail(url = self.audio_info[0][1])
      return embed
    else:
      print('uh oh')
    
  def create_embed(self):
    if len(self.audio_info) >= 1:
      embed = discord.Embed(title = '**Added | {}**'.format(self.audio_info[-1][0]), description = '{} successfully added a song to the queue | Position {} of {}'.format(self.audio_info[-1][2], len(self.song_queue), len(self.song_queue)), color = 0x000000)
      embed.set_thumbnail(url = self.audio_info[-1][1])
      return embed
    else:
      return None

  async def extract_audio(self, text):
    with YoutubeDL(YDL_OPTIONS) as ydl:
      try:
        get(' '.join(text)) 
      except:
        self.data = ydl.extract_info(f"ytsearch:{' '.join(text)}", download = False)['entries'][0]
      else:
        self.data = ydl.extract_info(' '.join(text), download = False)
      self.audio = await discord.FFmpegOpusAudio.from_probe(self.data['formats'][0]['url'], **FFMPEG_OPTIONS)
      self.song_queue.append(self.audio)
      self.audio_info.append((self.data.get('title'), self.data.get('thumbnail'), self.context.author.name.title()))
      await self.context.send(embed = self.create_embed())
      
  @commands.command(name = 'play', aliases = ['p', 'P', 'Play'])
  async def play(self, context, *args):
    self.context = context
    #await self.now_playing()
    if context.author.voice and not context.voice_client:
        await context.author.voice.channel.connect()
        await self.extract_audio(args)
        try:
          context.voice_client.play(self.song_queue[0])
          self.song_queue.pop(0)
          self.audio_info.pop(0)
        except:
          pass  
    else:
      await self.extract_audio(args)
      try:
        context.voice_client.play(self.song_queue[0])
        self.song_queue.pop(0)
        self.audio_info.pop(0)
      except:
        pass

  @commands.command(name = 'kick', aliases = ['k', 'K', 'Kick'])
  async def kick(self, context):
    if context.voice_client:
      self.song_queue = []
      self.audio_info = []
      await context.guild.voice_client.disconnect()

  @commands.command(name = 'skip', aliases = ['s', 'S', 'Skip'])
  async def skip(self, context):
    if context.author.voice:
      if context.author.voice:
        try:
          context.voice_client.stop()
          await context.send(embed = self.now_playing())
          self.context.voice_client.play(self.song_queue[0], after = lambda e: asyncio.run_coroutine_threadsafe(self.context.send(embed = self.now_playing()), CLIENT.loop))
          self.song_queue.pop(0)
          self.audio_info.pop(0)
        except:
          pass
        
async def setup(CLIENT):
  await CLIENT.add_cog(Music(CLIENT))
