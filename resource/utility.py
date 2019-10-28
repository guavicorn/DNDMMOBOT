import os
import json
import asyncio


def dict_to_class(dict_to_use):
    
    class from_dict:
        def __init__(self, target_dict):
            for key in target_dict:
                setattr(self, key, target_dict[key])

        def __repr__(self):
            return "{0}: {1}".format(self.__name__,self.__dict__)
    return from_dict(dict_to_use)


def loader(bot_folder, file_name=None, sub_folder=None):
    directory_path = "/home/pi/%s" % bot_folder
    if sub_folder is not None:
        directory_path += "/%s" % sub_folder
    if file_name is None:
        loadlist = []
        for file in os.listdir(directory_path):
            if file.endswith(".txt"):
                loadlist.append(file[:-4])
        else:
            return loadlist
    else:
        directory_path += "/%s" % file_name
        try:
            fileready = open(directory_path, "r")
        except FileNotFoundError:
            open(directory_path, "x")
            raise AttributeError
        else:
            fileset = fileready.read()
            return json.loads(fileset)


def saver(save_raw, bot_folder, file_name=None, sub_folder=None):
    directory_path = "/home/pi/%s" % bot_folder
    if sub_folder is not None:
        directory_path += "/%s" % sub_folder
    if file_name is None:
        pass
    else:
        directory_path += "/%s" % file_name
        if type(save_raw) is dict:
            save_dict = save_raw
        else:
            save_dict = dict(save_raw)
        filedump = json.dumps(save_dict)
        try:
            open(directory_path, "w")
        except FileNotFoundError:
            open(directory_path, "x")
        with open(directory_path, "w") as f:
            f.write(filedump)
            f.close()
    

async def sayandslice(ctx,client,question,check,wait_for_item='message',timeout=120):
    await ctx.send(question)
    message = await client.wait_for(wait_for_item, timeout=timeout, check=check)
    await ctx.channel.purge(limit=2,check=checks.fake)
    await asyncio.sleep(1)
    return message
