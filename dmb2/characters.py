import discord
from discord.ext import commands
import resource.embeds as embeds
import resource.checks as checks
import random as rand
import datetime

class Characters(commands.Cog):

    def __init__(self,client):
        self.client = client

    # Events
    @commands.Cog.listener("on_ready")
    async def on_example_ready(self):
        pass

    # Commands
    @commands.command(aliases=["gravestone"])
    @commands.guild_only()
    async def epitaph(self, ctx, *, char_name):

        await ctx.message.channel.purge(limit=1)

        def user_chk(m):
            return m.author.id == ctx.author.id

        def both_chk(m):
            return user_chk(m) or m.author.id == self.client.user.id

        await ctx.send("this is terrible news.. how old was %s?" % char_name)
        raw_char_age = await self.client.wait_for('message', check=user_chk)
        char_age = raw_char_age.content

        await ctx.message.channel.purge(limit=2, check=both_chk)

        await ctx.send("ah, i see.. what race and class was %s?" % char_name)
        raw_char_raceclass = await self.client.wait_for("message", check=user_chk)
        char_raceclass = raw_char_raceclass.content

        await ctx.message.channel.purge(limit=2, check=both_chk)

        await ctx.send("what word best describes %s" % char_name)
        raw_char_adj = await self.client.wait_for("message", check=user_chk)
        char_adj = raw_char_adj.content

        await ctx.message.channel.purge(limit=2, check=both_chk)

        await ctx.send("I am sure they were a %s soul.. now, describe something %s would be best known for." % (char_adj, char_name))
        raw_char_deed = await self.client.wait_for("message", check=user_chk)
        char_deed = raw_char_deed.content

        await ctx.message.channel.purge(limit=2, check=both_chk)

        graveyard_channel = discord.utils.find(lambda c: c.name == "cemetery", ctx.guild.text_channels)

        title = "Here Lies %s" % char_name
        desc_rand_adj = rand.choice(["rocked", "stole", "changed", "opened", "enriched"])
        desc_rand_item = rand.choice(["eyes", "hearts", "world", "minds", "lives"])
        description = "Only %s, %s was a %s %s who %s our %s by %s" % (char_age, char_name, char_adj, char_raceclass, desc_rand_adj, desc_rand_item, char_deed)
        footer_icon = "https://cdn.discordapp.com/attachments/633238657209335809/637431890592399370/gravestone.png"
        embed = embeds.embed(title=title, description=description, ftr_icon=footer_icon, ftr_text="Lain in the ground on", timestamp=datetime.datetime.utcnow().isoformat())
        await graveyard_channel.send("Another one falls...", embed=embed)

def setup(client):
    print('Characters Extension loaded successfully!')
    print("-----------------------------------------")
    client.add_cog(Characters(client))
