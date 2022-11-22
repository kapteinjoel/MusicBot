import music
import asyncio
from settings import *

if __name__ == '__main__':
  async def add_classes():
    for i in range(len(CLASSES)):
      await CLASSES[i].setup(CLIENT)

  @CLIENT.event
  async def on_ready():
    await add_classes()

  @CLIENT.event
  async def on_voice_state_update(member, before, after):
    if member.guild.voice_client is not None and len(member.guild.voice_client.channel.members) == 1:
        music.Music.song_queue = []
        music.Music.audio_info = []
        await member.guild.voice_client.disconnect()

CLIENT.run(TOKEN)
