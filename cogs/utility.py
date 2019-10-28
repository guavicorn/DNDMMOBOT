import discord
from discord.ext import commands
import resource.checks as checks

class Example(commands.Cog):

    def __init__(self,client):
        self.client = client

# -----------------------------------Events----------------------------------

    # runs when bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("%s logged in successfully!" % self.client.user.name)
        print("%s's ID is %d" % (self.client.user.name, self.client.user.id))
        print("-------------------------")

# ----------------------------------Commands---------------------------------

    # clears the chat, self explanatory
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clearchat(self, ctx, num_of_messages: int = 5):
        deleted = await ctx.channel.purge(limit=num_of_messages+1)
        await ctx.send("deleted %d messages from the channel" % len(deleted))    # Commands

    # bot echoes the attached message
    @commands.command()
    async def echo(self, ctx, *, message):
        await ctx.send(message)

def setup(client):
    client.add_cog(Example(client))
