import discord
from discord.ext import commands
import resource.checks as checks
import resource.embeds as embeds
import json
from random import randint
from time import time
from datetime import datetime
from typing import Union


# ------------------------------Single User Class------------------------------


class User:
    def __init__(self, user_id):

        # loads user data if it exists, creates it if it doesnt
        try:
            user_ready = open('/home/pi/bots/shared_data/users/%d.txt' % user_id, "r")
            user_set = user_ready.read()
            user_data = json.loads(user_set)
            user_data["id"] = user_id
            
        except FileNotFoundError:
            user_ready = open('/home/pi/bots/shared_data/users/example.txt', "r")
            user_set = user_ready.read()
            user_data = json.loads(user_set)
            user_data["id"] = user_id

            open("/home/pi/bots/shared_data/users/%d.txt" % user_id,"x")

            with open("/home/pi/bots/shared_data/users/%d.txt" % user_id,"w") as file:
                file.write(json.dumps(user_data))
                file.close()

        # sets class attributes from user_data dictionary
        for key in user_data:
                setattr(self, key, user_data[key])

    # saves user file
    def save(self):
        try:
            open("/home/pi/bots/shared_data/users/%d.txt" % self.id,"w")
        except FileNotFoundError:
            open("/home/pi/bots/shared_data/users/%d.txt" % self.id,"x")

        with open("/home/pi/bots/shared_data/users/%d.txt" % self.id,"w") as file:
            file.write(json.dumps(self.__dict__))
            file.close()


    # checks if user is at enough messages to level up
    def msg_check(self):
        self.message_count += 1
        if self.message_count == ((self.level + 1) ** 2) * 100:
            self.level += 1
            self.save()
            return True
        else:
            self.save()


    # sets users timezone
    def set_timezone(self, utc_offset):
        self.timezone = utc_offset
        self.save()


# ----------------------------------Users Cog----------------------------------


class Users(commands.Cog):

    def __init__(self,client):
        self.client = client


    # --------------------------- Converters -------------------------------


    class MemberRoles(commands.MemberConverter):
        async def convert(self, ctx, argument):
            member = await super().convert(ctx, argument)
            return [role.name for role in member.roles[1:]]

    class MemberGetter(commands.MemberConverter):
        async def convert(self, ctx, argument):
            member = await super().convert(ctx, argument)
            return member

    class RoleGetter(commands.RoleConverter):
        async def convert(self, ctx, argument):
            role = await super().convert(ctx, argument)
            return role


    # -------------------------------Events----------------------------------


    # runs when bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("Users extension loaded successfully!")
        print("-------------------------")


    # runs when a new message is seen by the bot
    @commands.Cog.listener("on_message")
    async def on_member_message(self, message):
        u = User(message.author.id)
        if type(message.channel) is discord.TextChannel:
            level_check = u.msg_check()
            if level_check:
                await message.channel.send("Congrats <@%d> youve reached chat level %d!" % (u.id,u.level))


    # runs when a user joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if "welcome" in self.client.extras.channels:
            welcome_channel = discord.utils.find(lambda c: c.name == self.client.extras.channels["welcome"])
        else:
            self.client.extras.channels["welcome"] = "welcome"
            welcome_channel = discord.utils.find(lambda c: c.name == self.client.extras.channels["welcome"])

        path = "/home/pi/bots/%s/messages/welcome.txt" % (self.client.extras.name)
        try:
            open(path,"r")
        except FileNotFoundError:
            open(path,"x")
            with open(path,"w") as file:
                file.write("Welcome @user!")
                file.close()
        welcome_message = open(path, "r").read().replace("@user", "<@%d>" % member.id)
        welcome_channel.send(self.client.extras)

    # ---------------------------------- Commands -----------------------------------


    # Checks when a user joined the server
    @commands.command()
    async def joined(self, ctx, *, member: discord.Member):
        await ctx.send('{0} joined on {0.joined_at}'.format(member))


    # creates a documented warning for a user
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, members: commands.Greedy[discord.Member], *, warning):

        # deletes command invoke message
        await ctx.channel.purge(limit=1)

        # iterates through members to individually warn them
        for member in members:

            # gathers user data for member
            mem = User(member.id)

            # sets up documented warning for saving
            warn_format = [ctx.author.name+"#"+ctx.author.discriminator, time(), warning]

            # creates discord embed to display warning to user
            warning_embed = embeds.embed(title="Official Warning #%s" % str(len(mem.warnings)+1),
                                         description='''you've been issued an official warning for the reason stated below.
if you feel this warning is unjust, please use `>appeal warning #` with # being the warning number.''',
                                         color=14483456,
                                         ftr_icon="https://cdn.discordapp.com/attachments/633238657209335809/633749426242060288/warning2.png",
                                         ftr_text="Warned by %s during" % warn_format[0],
                                         tmbnl_url="https://cdn.discordapp.com/attachments/633238657209335809/633749425986207794/warning.png",
                                         timestamp=datetime.utcfromtimestamp(warn_format[1]).isoformat(),
                                         fields=[embeds.fldformat("Warning Reason", warning)])

            # creates a direct message channel if one does not exist
            if member.dm_channel is None:
                await member.create_dm()

            await member.dm_channel.send(embed=warning_embed)

            # adds warning to user file
            mem.warnings.append(warn_format)

            mem.save()
        
            print("%s has been warned" % member.name)
            await ctx.send("<@%d> has been warned." % member.id)


    # displays user's current warnings
    @commands.command()
    @commands.guild_only()
    async def warnings(self, ctx, members: commands.Greedy[discord.Member]=None):

        # discord embed color uses hex converted to integer
        embed_color = 56816

        # Sets Command invoker as the search target for warnings if one is not set
        if members is None:
            members = [ctx.author]

        # Makes sure a single member still ends up in a list
        elif type(members) == discord.Member:
            members = [members]

        # iterates through members to individually find warnings
        for member in members:

            # gathers user data for member
            mem = User(member.id)

            # lowering green value from future embed colors, to make a color change effect
            embed_color -= 4096

            # temporary warning counter for use in sending messages
            warning_count = 0

            # iterates through members warnings and displays them
            for warning in mem.warnings:
                warning_count += 1

                # Makes sure warning has an author, sets to unknown if not
                if warning[0] is None or warning[0] == "":
                    warning_author_name = "Uknown Author"
                else:
                    warning_author_name = warning[0]

                # creating a discord embed for warning to display in
                warning_embed = embeds.embed(title="**%s's Warnings**" % member.name,
                                             description="Warning %d of %d" % (mem.warnings.index(warning) + 1, len(mem.warnings)),
                                             color=embed_color,
                                             ftr_icon="https://cdn.discordapp.com/attachments/633238657209335809/633749426242060288/warning2.png",
                                             ftr_text="Warned by %s during" % warning_author_name,
                                             tmbnl_url="https://cdn.discordapp.com/attachments/633238657209335809/633749425986207794/warning.png",
                                             timestamp=datetime.utcfromtimestamp(warning[1]).isoformat(),
                                             fields=[embeds.fldformat("**Warning Reason**",warning[2])])

                await ctx.send(embed=warning_embed)

                # lowering blue value of future embeds for color change effect
                embed_color -= 15


    # kicks a user with specified reason
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):

        if reason is None:
            await ctx.send("You must state a reason to kick them before i will do anything.")
        else:
            for member in members:
                await ctx.channel.purge(limit=1)
                if member.dm_channel is None:
                    await member.create_dm()
                await member.dm_channel.send("You have been kicked for %s" % reason)
                await ctx.send("Kicking <@%d> now..." % member.id)
                await member.kick(reason=reason)

    # bans a user with specified reason
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        await ctx.channel.purge(limit=1,checks=checks.fake)
        await ctx.send("Banning <@%d> now.." % member.id)
        await member.ban(reason=reason)


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):

        await ctx.channel.purge(limit=1,checks=checks.fake)

        banned_users = await ctx.guild.bans()

        if "#" in member:
            member_name, member_discriminator = member.split("#")

        else:
            member_name = member
            member_discriminator = None
        
        for ban_entry in banned_users:
            user = ban_entry.user

            if member_discriminator is None:
                if user.name == member_name:
                    await ctx.guild.unban(user)
                    await ctx.send('Unbanned %s#%d' % (user.name,user.discriminator))
                    return
            else:
                if (user.name,user.discriminator) == (member_name,member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send('Unbanned %s#%d' % (user.name,user.discriminator))
                    return

    @commands.command(aliases=["+rep","plusrep"])
    async def addrep(self, ctx, member: discord.Member, *, reason):
        mem = User(member.id)
        for category in mem.reputation:
            for rep in mem.reputation[category]:
                if rep[0] == ctx.author.id:
                    del mem.reputation[category][mem.reputation[category].index(rep)]
        else:
            mem.reputation["accepted"].append([ctx.author.id,time.today()])


def setup(client):
    client.add_cog(Users(client))
