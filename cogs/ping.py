import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.slash_command()
    async def ping(self, ctx):
        # if ctx.author.guild_permissions.administrator:
        # else:
        #     await ctx.respond("You don't have permission to use this command.")
        await ctx.respond(
            embed=discord.Embed(
                title="Pong!",
                description=f"Latency is {round(self.client.latency * 1000)}ms",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )


def setup(client):
    client.add_cog(Ping(client))
