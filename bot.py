import discord, json, os, sys
sys.path.append("./utils")
from utils.database import DataBase
from discord.ext import commands

# ? bot init
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ? variabls
CONFIG = json.load(open("./config.json"))
TOKEN = CONFIG["TOKEN"]


for pyFile in os.listdir("./cogs"):
    if pyFile.endswith(".py"):
        bot.load_extension(f"cogs.{pyFile[:-3]}")


@bot.event
async def on_guild_remove(guild):
    DataBase().delete_server(server_id=guild.id)
    print(f"Left or was kicked from server: {guild.name}")

@bot.event
async def on_guild_join(guild):
    DataBase().create_server(server_id=guild.id, server_name=guild.name)
    print(f"joined from server: {guild.name}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


bot.run(TOKEN)
