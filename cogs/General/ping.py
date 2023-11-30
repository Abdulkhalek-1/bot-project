import discord


class Ping(discord.Cog):
    def __init__(self, client):
        self.client = client

    @discord.guild_only()
    @discord.slash_command()
    async def ping(self, ctx):
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
