import resource.url_stuff as urls
from discord.ext import commands
from discord import TextChannel as discTextChannel

# ---------------- Basic Checks ----------------

# A fake check that just returns True
def fake(message):
    return True

# A check
def num(message):
    return message.content.isdigit()

def colornum(message):
    if message.content.isdigit():
        return int(message.content) <= 16777215

def none(message):
    if message.content.lower() == "none":
        message.content = None
        return True

def rand(message):
    return message.content.lower() == "random"

def field(message):
    return " - " in message.content

def numnone(message):
    return numchk(message) or nonechk(message)

def mem(message):
    return message.author.id == 0

def yes(message):
    return message.content.lower().replace(".","") in ["y","yes","yep","yeah","yea","ye","yee","yeee","yae","mhm","sure","sure is","absolutely","roger","roger that","copy","copy that","totally","totaly","yeap","yye","positive"]

def no(message):
    return message.content.lower().replace(".","") in ["n","no","na","nah","nope","neh","nnah","nop","negative","not a chance","noo","nooo","noooo"]

def yesno(message):
    return yeschk(message) or nochk(message)

def self(message):
    return message.author.id == 569571334485704704

def url(message):
    if nonechk(message):
        return True
    space_split_list = message.content.split(" ")
    for split_piece in space_split_list:
        if split_piece == "":
            space_split_list.remove(split_piece)
        if len(space_split_list) == 1:
            for ii in optim.url_endings:
                if ".%s/" % ii in i:
                    return True

def imgurl(message):
    if nonechk(message):
        return True
    space_split = message.content.split(" ")
    for split_piece in space_split:
        if split_piece == "":
            space_split.remove(split_piece)
        if len(space_split) == 1:
            for url_ending in urls.url_endings:
                if ".%s/" % url_ending in split_piece:
                    for file_extension in ["jpg","png","bmp","gif"]:
                        if ".%s" % file_extention in split_piece:
                            return True

def direct_message(message):
    if type(message.channel) is not discTextChannel:
        return True



# ---------------- Decorator Checks ----------------

class NoPrivateMessages(commands.CheckFailure):
        pass

def in_guild(guild_id=None):
    if guild_id is None:
        async def predicate(ctx):
            if ctx.guild is None:
                raise NoPrivateMessages('This Command only works from inside a guild, Private Messages will not work with this command.')
            return True
    else:
        async def predicate(ctx):
            if ctx.guild.id == guild_id:
                raise NoPrivateMessages('This Command only works from inside the {} server, Private Messages or messages in another server will not work with this command.'.format(ctx.guild.name))
            return True
    return commands.check(predicate)

def is_admin():
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessages('This Command only works from inside a guild, Private Messages will not work with this command.')
        else:
            if ctx.author.top_role == bot.guild:
                pass
