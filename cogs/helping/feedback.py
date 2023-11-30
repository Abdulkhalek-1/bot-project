import sys, discord

sys.path.append("../utils")
from database import DataBase


class EmptyCog4(discord.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(EmptyCog4(client))
