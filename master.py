import discord, asyncio
from discord.ext import commands, tasks
from os import listdir
import json
from resource.utility import dict_to_class

# sets which bot files to access
print("Input Bot Name.\n")
bot_name = input()


try:

    # opens bot file if it exists
    bot_ready = open("/home/pi/bots/%s/bot.txt" % bot_name, "r")
    bot_set = bot_ready.read()

    # loads up the data in bot file as a class
    bot_data = dict_to_class(json.loads(bot_set))
    bot_data.name = bot_name

except FileNotFoundError:
    
    # if bot file does not exist, the file is created here
    open("/home/pi/bots/%s/bot.txt" % bot_name, "x")

    # open newly created file
    with open("/home/pi/bots/%s/bot.txt" % bot_name, "w") as file:

        # entering a token for the bot to use
        print("Enter a Token for %s to use.\n" % bot_name)
        bot_token = input()

        # sets bot file data basics, and makes a class from it
        bot_data = dict_to_class({"lifetime":0,"prefix":{"on_join":">"},"extensions":["users","utility"],"token":bot_token})
        bot_data.name = bot_name
        file.write(json.dumps(bot_data.__dict__))
        file.close()

# saves data to a bot file
def saver(client):
    
    # checks for existence of the bot file
    try:
        open("/home/pi/bots/%s/bot.txt" % client.extras.name, "w")

    # creates bot file if it does not exist
    except FileNotFoundError:
        open("/home/pi/bots/%s/bot.txt" % client.extras.name, "x")

    # opens the bot file and saves data to it
    with open("/home/pi/bots/%s/bot.txt" % client.extras.name, "w") as file:
        file.write(json.dumps(client.extras.__dict__))
        file.close()

# command prefix getter
def prefix_getter(client, message):

    # opens bot file
    bot_ready = open("/home/pi/bots/%s/bot.txt" % bot_name, "r")
    bot_set = bot_ready.read()

    # loads up the data in bot file as a class
    bdata = dict_to_class(json.loads(bot_set))
    if str(message.guild.id) in bdata.prefix:
        return bdata.prefix[str(message.guild.id)]
    else:
        bdata.prefix[str(message.guild.id)] = ">"
        return bdata.prefix[str(message.guild.id)]


# sets the command prefix for the bot
client = commands.Bot(command_prefix=prefix_getter)

client.extras = bot_data

client.save_extras = saver

@client.event
async def on_ready():
    print("%s logged in successfully!" % client.user.name)
    print("{0.name}'s ID is {0.id}".format(client.user))
    print("{0.extras.name} set as {0.user.name}'s directory".format(client))

@tasks.loop(minutes=5)
async def reload_bot_file():
    client.save_extras(client)
    
    # opens bot file if it exists
    bot_ready = open("/home/pi/bots/%s/bot.txt" % bot_name, "r")
    bot_set = bot_ready.read()

    # loads up the data in bot file as a class
    client.extras = dict_to_class(json.loads(bot_set))
    client.extras.name = bot_name

# ----------------------------------Commands-----------------------------------

@client.group(name="cogs")
async def _cogs(ctx):
    if ctx.invoked_subcommand is None:
        if " " in ctx:
            await ctx.send("I dont know that subcommand")
        else:
            await ctx.send("use `%shelp cogs` to understand how to use this command" % bot_data.prefix)


# command to load Extensions
@_cogs.command()
async def load(ctx, *, extensions):

    if type(ctx.channel) == discord.TextChannel:
            await ctx.channel.purge(limit=1)

    # breaks space divided list into actual list
    ext_list = [ext for ext in extensions.split(" ")]

    for extension in ext_list:
        
        # checks if extension is in the common cogs folder
        if extension+".py" in listdir("/home/pi/bots/cogs/"):

            try:
                # loads extension if possible
                client.load_extension("cogs.%s" % extension)

                # checks if extension is listed already in bot file
                if extension not in client.bot_data.extensions:

                    # if not the extension is added to the list
                    client.extras.extensions.append(extension)

                    # redundently makes sure bot file exists
                    try:
                        with open("/home/pi/bots/%s/bot.txt" % client.extras.name, "w") as file:
                            file.write(json.dumps(client.extras.__dict__))
                            file.close()

                    # redundently creates bot file if it does not exist
                    except FileNotFoundError:
                        open("/home/pi/bots/%s/bot.txt" % client.extras.name, "x")
                        with open("/home/pi/bots/%s/bot.txt" % client.extras.name, "w") as file:
                            file.write(json.dumps(client.extras.__dict__))
                            file.close()

            # Catch-all error handler
            except:
                await ctx.send("Sorry, something went wrong.")

            else:
                await ctx.send("Successfully loaded the %s extension!" % extension)

        #if extension not in common cogs, check if extension in bot specific folder
        elif extension+".py" in listdir("/home/pi/bots/%s/" % client.extras.name):
            try:
                client.load_extension("%s.%s" % (client.extras.name, extension))
            except:
                await ctx.send("Something went wrong, sorry about that")
            else:
                await ctx.send("Successfully loaded the %s extension!" % extension)

        print("Successfully loaded the %s extension!" % extension)

# command to unload extensions from bot
@_cogs.command()
async def unload(ctx, extensions):

    # list of extensions
    ext_list = [ext for ext in extensions.split(" ")]

    #iterate through extensions to unload them individually
    for extension in ext_list:
        try:
            client.unload_extension("cogs.%s" % extension)
            await ctx.send("Unloaded the %s extension" % extension)

            # deletes extension from bot startup extension list if it exists
            if extension in client.extras.extensions:
                del client.extras.extensions[client.extras.extensions.index(extension)]

                with open("/home/pi/bots/%s/bot.txt" % client.extras.name, "w") as file:
                    file.write(json.dumps(client.extras.__dict__))
                    file.close()

        # tries to unload cog from bot directory if its not in common cogs
        except:
            try:
                client.unload_extension("%s.%s" % (client.extras.name, extension))

            # error handler
            except:
                await ctx.send("Sorry, something went wrong. I probably don't have that cog loaded")

@_cogs.command()
async def reload(ctx, extensions):

    # list of extensions
    ext_list = [ext for ext in extensions.split(" ")]

    # iterates through extensions to individually reload them
    for extension in ext_list:
        try:
            # checking the location of the cog before reloading
            if extension in client.extras.extensions and extension+".py" in listdir("/home/pi/bots/cogs/"):
                client.unload_extension("cogs.%s" % extension)
                client.load_extension("cogs.%s" % extension)
                await ctx.send("Successfully reloaded the %s extension!" % extension)
            elif extension+".py" in listdir("/home/pi/bots/%s/" % client.extras.name):
                client.unload_extension("%s.%s" % (client.extras.name, extension))
                client.load_extension("%s.%s" % (client.extras.name, extension))
                await ctx.send("Successfully reloaded the %s extension!" % extension)
            else:
                await ctx.send("%s is not a loaded cog." % extension)

        # error handler
        except:
            await ctx.send("Something went wrong when loading the cog.")

# loads all cogs in startup extension list
for extension in client.extras.extensions:
    client.load_extension("cogs.%s" % extension)

# loads up all cogs the bot can see in the bot directory
for file in listdir("/home/pi/bots/%s/" % client.extras.name):
    if file.endswith(".py") and file != "__init__.py" and not file.startswith("h_"):
        client.load_extension("%s.%s" % (client.extras.name, file[:-3]))

# runs the bot using token listed in bot file
client.run(client.extras.token)
