import discord
from discord.ext import commands
from json import loads, dumps
from os import listdir

class Suggestions(commands.Cog):

    def __init__(self,client):
        self.client = client

    # -----------------------------Events----------------------------------


    @commands.Cog.listener("on_message")
    async def on_suggestion(self, message):

        # checks if message is in a voting channel
        if type(message.channel) == discord.TextChannel:
            if message.channel.name in self.client.extras.channels["suggestions"]:

                suggestion = {"author_id": message.author.id, "suggestion_text": message.content}

                if "1⃣" in message.content:
                    suggestion["1⃣"] = 0
                    await message.add_reaction("1⃣")

                    if "2⃣" in message.content:
                        suggestion["2⃣"] = 0
                        await message.add_reaction("2⃣")

                        if "3⃣" in message.content:
                            suggestion["3⃣"] = 0
                            await message.add_reaction("3⃣")

                            if "4⃣" in message.content:
                                suggestion["4⃣"] = 0
                                await message.add_reaction("4⃣")

                                if "5⃣" in message.content:
                                    suggestion["5⃣"] = 0
                                    await message.add_reaction("5⃣")

                else:
                    await message.add_reaction("\U0001F44D")
                    suggestion["\U0001F44D"] = 0
                await message.add_reaction("\U0001F44E")
                suggestion["\U0001F44E"] = 0
                await message.add_reaction("\u270b")
                suggestion["\u270b"] = 0

                open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, message.channel.name, message.id), "x")
                with open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, message.channel.name, message.id), "w") as file:
                    file.write(dumps(suggestion))
                    file.close()

    @commands.Cog.listener("on_message_edit")
    async def on_suggestion_edit(self,before,after):

        # checks if message is in a voting channel
        if type(before.channel) == discord.TextChannel:

            if before.channel.name in self.client.extras.channels["suggestions"]:

                suggestion = {}

                try:
                    suggestion_ready = open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, before.channel.name, before.id), "r")
                    suggestion = loads(suggestion_ready.read())
                except FileNotFoundError:
                    open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, before.channel.name, before.id), "x")

                if "1⃣" in after.content:
                    if "\U0001F44D" in suggestion:
                        await after.remove_reaction("\U0001F44D", self.client.user)
                        del suggestion["\U0001F44D"]
                        suggestion["1⃣"] = 0
                        await after.add_reaction("1⃣")

                        if "2⃣" in after.content:
                            suggestion["2⃣"] = 0
                            await after.add_reaction("2⃣")

                            if "3⃣" in after.content:
                                suggestion["3⃣"] = 0
                                await after.add_reaction("3⃣")

                                if "4⃣" in after.content:
                                    suggestion["4⃣"] = 0
                                    await after.add_reaction("4⃣")

                                    if "5⃣" in after.content:
                                        suggestion["5⃣"] = 0
                                        await after.add_reaction("5⃣")

                try:
                    open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, before.channel.name, before.id), "w")
                except FileNotFoundError:
                    open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, before.channel.name, before.id), "x")

                with open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, before.channel.name, before.id), "w") as file:
                    file.write(dumps(suggestion))
                    file.close()

    # runs when a user reacts to a message in role-react and adds that role
    @commands.Cog.listener("on_raw_reaction_add")
    async def on_vote_add(self, payload):

        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)
        member = guild.get_member(payload.user_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        print("User voted %s" % payload.emoji.name)

        if channel.name in self.client.extras.channels["suggestions"]:

            if str(message.id) in listdir("/home/pi/bots/%s/suggestions/%s/" % (self.client.extras.name, channel.name)) and payload.user_id != self.client.user.id:

                suggestion = open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, channel.name, message.id), "r")

                vote_data = {}

                try:
                    vote_data = loads(open("/home/pi/bots/%s/suggestions/%s/info.txt" % (self.client.extras.name, channel.name),"r").read())
                except FileNotFoundError:
                    vote_data = {"roles": ["Demi Council", "God"], "majority_mod": 0.75, "count_time":"friday"}

                for role in member.roles:

                    if role.name in vote_data["roles"]:
                        suggestion[str(payload.emoji)] += 1
                        with open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, channel.name, message.id), "w") as file:
                            file.write(dumps(suggestion))
                            file.close()
                        break
                else:
                    message.remove_reaction(payload.emoji, member)


    # runs when a user reacts to a message in role-react and adds that role
    @commands.Cog.listener("on_raw_reaction_remove")
    async def on_vote_remove(self, payload):
        
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)
        member = guild.get_member(payload.user_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        print("User removed vote %s" % payload.emoji.name)

        if channel.name in self.client.extras.channels["suggestions"]:
            if str(message.id) in listdir("/home/pi/bots/%s/suggestions/%s/" % (self.client.extras.name, channel.name)) and payload.user_id != self.client.user.id:

                suggestion = open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, channel.name, message.id), "r")

                vote_data = {}

                try:
                    vote_data = loads(open("/home/pi/bots/%s/suggestions/%s/info.txt" % (self.client.extras.name, channel.name),"r").read())
                except FileNotFoundError:
                    vote_data = {"roles": ["Demi Council", "God"], "majority_mod": 0.75, "count_day":4}

                for role in member.roles:

                    if role.name in vote_data["roles"]:
                        suggestion[str(payload.emoji)] -= 1
                        with open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (self.client.extras.name, channel.name, message.id), "w") as file:
                            file.write(dumps(suggestion))
                            file.close()
                        break

    # ---------------------------Converters--------------------------------

    class ChannelGetter(commands.TextChannelConverter):
        async def convert(self, ctx, argument):
            channel = await super().convert(ctx, argument)
            return channel

    # ----------------------------Commands---------------------------------

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def suggestionchannel(self, ctx, channel: ChannelGetter):
        
        if "channels" in self.client.extras.__dict__:

            if "suggestions" in self.client.extras.channels:
                if not channel.name in self.client.extras.channels["suggestions"]:
                    self.client.extras.channels["suggestions"].append(channel.name)
                else:
                    indexed = self.client.extras.channels["suggestions"].index(channel.name)
                    del self.client.extras.channels["suggestions"][indexed]

            else:
                self.client.extras.channels["suggestions"] = [channel.name]

        else:
            self.client.extras.channels = {"suggestions":[channel.name]}

        self.client.save_extras()
        await ctx.send("Added %s to the suggestions channels" % channel.name)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def accept(self, ctx, channel_name, message_id):
        try:
            open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (client.extras.name, channel_name, message_id), "r")
        except FileNotFoundError:
            await ctx.send("i dont see that suggestion there")
        suggestion = {}
        with open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (client.extras.name, channel_name, message_id), "r") as file:
            suggestion = loads(file.read())
            file.close()

        open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (client.extras.name, "accepted", message_id), "x")

        with open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (client.extras.name, "accepted", message_id), "w") as file:
            file.write(dumps(suggestion))
            file.close()

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def reject(self, ctx, channel_name, message_id):
        try:
            open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (client.extras.name, channel_name, message_id), "r")
        except FileNotFoundError:
            await ctx.send("i dont see that suggestion there")
        suggestion = {}
        with open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (client.extras.name, channel_name, message_id), "r") as file:
            suggestion = loads(file.read())
            file.close()

        open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (client.extras.name, "rejected", message_id), "x")

        with open("/home/pi/bots/%s/suggestions/%s/%d.txt" % (client.extras.name, "rejected", message_id), "w") as file:
            file.write(dumps(suggestion))
            file.close()

def setup(client):
    client.add_cog(Suggestions(client))
    print("Suggestions extension loaded in successfully!")
    print("-------------------------")
