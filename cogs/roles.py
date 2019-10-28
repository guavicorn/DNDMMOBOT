import discord
from discord.ext import commands

class Roles(commands.Cog):

    def __init__(self,client):
        self.client = client

    # -----------------------------Converters-----------------------------

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

    # -------------------------------Events-------------------------------

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if type(message.channel) == discord.TextChannel:
            if message.channel.name == "role-react":
                self.client.extras.react_roles[str(message.id)] = []
                for reactrole in self.client.extras.react_roles["unbound"]:
                    await message.add_reaction(reactrole[0].encode("utf-16").decode("utf-16"))
                    self.client.extras.react_roles[str(message.id)].append(reactrole)
                self.client.save_extras(self.client)

    # runs when a user reacts to a message in role-react and adds that role
    @commands.Cog.listener("on_raw_reaction_add")
    async def role_reaction_add(self, payload):

        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)

        member = guild.get_member(payload.user_id)

        if str(payload.message_id) in self.client.extras.react_roles and payload.user_id != self.client.user.id:
            base_roles = [discord.utils.find(lambda r: r.name == r_name, guild.roles) for r_name in self.client.extras.react_roles["base_roles"]]
            for rolereact in self.client.extras.react_roles[str(payload.message_id)]:
                if payload.emoji.name.encode("unicode-escape").decode("utf-16") == rolereact[0].encode("unicode-escape").decode("utf-16"):
                    for role in guild.roles:
                        if role.name == rolereact[1]:
                            print("Adding {0.name} role to {1.name}#{1.discriminator}".format(role, member))
                            await member.add_roles(role)
                            if len(base_roles) != 0:
                                for r in base_roles:
                                    await member.remove_roles(r)

                            # creates direct message with user if it doesnt exist
                            if member.dm_channel is None:
                                await member.create_dm()

                            # tells user they got a role through Direct Messages
                            await member.dm_channel.send("I've added the %s role for you! to have the role removed at any time just take away your reaction from the message in #role-react" % role.name)

                            # sends role info if it exists
                            try:
                                await member.dm_channel.send(open("/home/pi/bots/%s/roles/%s.txt" % (self.client.extras.name, rolereact[1].replace(" ", "_").replace("'","")),"r").read())
                            except FileNotFoundError:
                                pass
                            
                            break

    # runs when a user reacts to a message in role-react and adds that role
    @commands.Cog.listener("on_raw_reaction_remove")
    async def role_reaction_remove(self, payload):
        
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)

        member = guild.get_member(payload.user_id)

        if str(payload.message_id) in self.client.extras.react_roles and payload.user_id != self.client.user.id:
            base_roles = [discord.utils.find(lambda r: r.name == r_name, guild.roles) for r_name in self.client.extras.react_roles["base_roles"]]

            for rolereact in self.client.extras.react_roles[str(payload.message_id)]:
                if payload.emoji.name.encode("unicode-escape").decode("utf-16") == rolereact[0].encode("unicode-escape").decode("utf-16"):
                    for role in guild.roles:
                        if role.name == rolereact[1]:

                            print("Removing {0.name} role to {1.name}#{1.discriminator}".format(role, member))

                            await member.remove_roles(role)

                            if len(base_roles) != 0:
                                for r in base_roles:
                                    await member.add_roles(r)

                            if member.dm_channel is None:
                                await member.create_dm()

                            await member.dm_channel.send("I've removed the %s role for you! to have the role added back at any time just react to the message in #role-react" % role.name)

                            break

    # ------------------------------Commands------------------------------
    
    # Checks what roles a user has
    @commands.command()
    @commands.guild_only()
    async def rolecheck(self, ctx, *, member: MemberRoles):
        await ctx.send('I see the following roles:\n> ' + '\n> '.join(member))

    # Adds a role to invoker, so long as its neither admin/higher permission role than currently possessed
    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, *, role: RoleGetter):
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.send("I have removed the %s role from you!" % role.name)
        else:
            if role in ctx.guild.roles:
                if role.permissions <= ctx.author.top_role.permissions and role.permissions.administrator == False:
                    await ctx.author.add_roles(role)
                    await ctx.send("I have added the %s role to you, <@%d>!"% (role.name, ctx.author.id))
                elif role.permissions.administrator == True:
                    await ctx.send("I respect you for trying but no. \U0001f609")
                else:
                    await ctx.send("You don't have access to that role.")
            else:
                await ctx.send("I don't see that role on this server, maybe you mispelled it?")


    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def newrole(self, ctx, *, name):
        for role in ctx.guild.roles:
            if role.name == name:
                await ctx.send("theres already a role with that name")
                break
        else:
            await ctx.guild.create_role(name, discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))


    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def addreactrole(self, ctx, emoji, role_name, *, role_info):
        if "react_roles" in self.client.extras.__dict__:
            self.client.extras.react_roles["unbound"].append([str(emoji), role_name])
        else:
            self.client.extras.react_roles = {"unbound":[[str(emoji), role_name]]}
        await ctx.send("Linked the %s emoji to the %s role!" % (str(emoji), role_name))

        # path to role info file
        path = "/home/pi/bots/%s/roles/%s.txt" % (self.client.extras.name, role_name.replace(" ","_").replace("'",""))

        # tries to load file at path, creating it if it doesnt find one
        try:
            open(path, "w")
        except FileNotFoundError:
            open(path, "x")

        # bot writes the roles info into a text file
        with open(path, "w") as role_file:
            role_file.write(role_info)
            role_file.close()

        # saves the dynamic data to the bot file
        self.client.save_extras(self.client)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def setbaserole(self, ctx, *, role_name):
        if role_name not in self.client.extras.react_roles["base_roles"]:
            if "base_roles" in self.client.extras.react_roles:
                self.client.extras.react_roles["base_roles"].append(role_name)
            else:
                self.client.extras.react_roles["base_roles"] = [role_name]
            self.client.save_extras(self.client)


def setup(client):
    client.add_cog(Roles(client))
    print("roles extension loaded successfully!")
    print("------------------------------------")
