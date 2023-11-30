import sys, discord

sys.path.append("../utils")
from database import DataBase


class EmptyCog7(discord.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(EmptyCog7(client))
