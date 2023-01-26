import discord, os, music, task_about, task_enroller, task_adder
from discord.ext import commands

#static setup related variables
CLASSES = [music, task_about, task_enroller, task_adder]
TOKEN = os.environ['TOKEN']
INTENTS, INTENTS.members = (discord.Intents.all(), True)
CLIENT = commands.Bot(intents=INTENTS, command_prefix='>')