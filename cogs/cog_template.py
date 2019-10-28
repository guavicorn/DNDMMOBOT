import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self,client):
        self.client = client

    # Events
    @commands.Cog.listener("on_ready")
    async def on_example_ready(self):
        print("%s logged in successfully!" % client.user.name)
        print("%s's ID is %d" % (client.user.name, client.user.id))
        print("-------------------------")

    # Commands
    @commands.command()
    async def echo(self, ctx, *, message):
        await ctx.send(message)

def setup(client):
    client.add_cog(Example(client))
