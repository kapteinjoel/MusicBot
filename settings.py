import discord, os, music
from discord.ext import commands

#static setup related variables
CLASSES = [music]
TOKEN = os.environ['TOKEN']
INTENTS, INTENTS.members = (discord.Intents.all(), True)
CLIENT = commands.Bot(intents=INTENTS, command_prefix='>')
