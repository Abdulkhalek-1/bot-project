import discord, json, os, sys, sqlite3
sys.path.append("./utils")
from discord.ext import commands
from database import DataBase
from cogs.TempVoice.temp_voice import TempRoomControlView

# ? bot init
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ? variabls
CONFIG = json.load(open("./config.json"))
TOKEN = CONFIG["TOKEN"]

# ? Cogs loader
for root, _, files in os.walk("./cogs"):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            try:
                cog_dir = f"{file_path[2:-3].replace(os.path.sep, '.')}"
                bot.load_extension(cog_dir)
                # print(f"{file_path[2:-3].replace(os.path.sep, '.')}")
            except Exception as e:
                print(
                    f"""
Error while loading {cog_dir}
Error: {e}
"""
                )


# ? database operations
def guilds_register(guilds):
    guilds = [(guild.id, guild.name) for guild in guilds]
    for id, name in guilds:
        DataBase().create_server(server_id=id, server_name=name)


@bot.event
async def on_guild_remove(guild):
    DataBase().delete_server(server_id=guild.id)


@bot.event
async def on_guild_join(guild):
    DataBase().create_server(server_id=guild.id, server_name=guild.name)


@bot.event
async def on_ready():
    guilds_register(bot.guilds)
    # bot.add_view(TempRoomControlView())
    print(f"\n\nLogged in as {bot.user.name}")


bot.run(TOKEN)
