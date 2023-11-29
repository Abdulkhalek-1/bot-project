# import discord
# from discord.ext import commands

# def say_hello(msg):
#     responses = {
#         "السلام عليكم": "عليكم السلام يا ",
#         "hello": "hello, ",
#         "welcome": "welcome, ",
#     }
#     return responses[msg] if msg in list(responses.keys()) else None

# class SayHello(commands.Cog):
#     def __init__(self, client):
#         self.client = client
    
#     @commands.Cog.listener()
#     async def on_message(self, message):
#         if message.author == self.client.user:
#             return
#         if say_hello(user_msg.strip().lower()):
#             await channel.send(
#                 f"{say_hello(user_msg.strip().lower())}{msg.author.mention}"
#             )


# def setup(client):
#     client.add_cog(SayHello(client))

import discord
from discord.ext import commands

def say_hello(msg):
    responses = {
        "السلام عليكم": "عليكم السلام يا ",
        "hello": "hello, ",
        "welcome": "welcome, ",
    }
    return responses.get(msg, None)

class SayHello(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        user_msg = message.content.strip().lower()
        response = say_hello(user_msg)

        if response:
            await message.channel.send(f"{response}{message.author.mention}")

def setup(client):
    client.add_cog(SayHello(client))
