import resource.trng as rand
import discord
import datetime

def fldformat(name, value, inline=False):
    return {"name": name, "value": value, "inline": inline}


def embed(
    title=None,
    description=None,
    url=None,
    color=rand.randbelow(0,16777215),
    ftr_icon=None,
    ftr_text=None,
    tmbnl_url=None,
    img_url=None,
    athr_name=None,
    athr_url=None,
    athr_icon_url=None,
    timestamp=None,
    fields=None):
    embed_dict = {
        "title": title,
        "description": description,
        "url": url,
        "color": color,
        "footer": {"icon_url": ftr_icon, "text": ftr_text},
        "thumbnail": {"url": tmbnl_url},
        "image": {"url": img_url},
        "author": {"name": athr_name, "url": athr_url, "icon_url": athr_icon_url},
        "timestamp": timestamp,
        "fields":fields}
    embed_dict2 = {
        "title": title,
        "description": description,
        "url": url,
        "color": color,
        "footer": {"icon_url": ftr_icon, "text": ftr_text},
        "thumbnail": {"url": tmbnl_url},
        "image": {"url": img_url},
        "author": {"name": athr_name, "url": athr_url, "icon_url": athr_icon_url},
        "timestamp": timestamp,
        "fields":fields}
    
    for i in embed_dict2:
        if embed_dict2[i] is None:
            del embed_dict[i]
        elif i == "timestamp" and embed_dict2[i] == "now":
            embed_dict[i] = datetime.datetime.utcnow().isoformat()
        elif i == "timestamp" and not embed_dict2[i].lower().endswith("z"):
            if embed_dict2[i] == "":
                del embed_dict[i]
            else:
                embed_dict[i] = embed_dict2[i]
        elif i == "thumbnail":
            if embed_dict2[i]["url"] is None or embed_dict2[i]["url"].lower() == "none":
                del embed_dict[i]
        elif i == "image":
            if embed_dict2[i]["url"] is None or embed_dict2[i]["url"].lower() == "none":
                del embed_dict[i]
        elif i == "author":
            if embed_dict2[i]["url"] is None or embed_dict2[i]["url"].lower() == "none":
                del embed_dict[i]["url"]
            if embed_dict2[i]["icon_url"] is None or embed_dict2[i]["icon_url"].lower() == "none":
                del embed_dict[i]["icon_url"]
            if embed_dict2[i]["name"] is None or embed_dict2[i]["name"].lower() == "none":
                del embed_dict[i]
        elif i == "footer":
            if embed_dict2[i]["icon_url"] is None or embed_dict2[i]["icon_url"].lower() == "none":
                del embed_dict[i]["icon_url"]
            if embed_dict2[i]["text"] is None or embed_dict2[i]["text"].lower() == "none":
                del embed_dict[i]
        elif i == "fields":
            if embed_dict2[i] == []:
                del embed_dict[i]
        elif embed_dict2[i] is str:
            if embed_dict2[i].lower() == "none":
                del embed_dict[i]
    else:
        return discord.Embed.from_dict(embed_dict)

def embed2(
    title=None,
    description=None,
    title_url=None,
    color=None,
    footer_icon_url=None,
    footer_text=None,
    thumbnail_url=None,
    image_url=None,
    author_name=None,
    author_url=None,
    author_icon_url=None,
    fields=None):
    embed = discord.Embed()
    if color is None:
        embed = discord.Embed(title=title,description=description,color=rand.randbelow(0,16777215),url=title_url,timestamp=datetime.datetime.utcnow())
    else:
        embed = discord.Embed(title=title,description=description,color=color,url=title_url,timestamp=datetime.datetime.utcnow())
    if image_url is not None:
        embed.set_image(url=image_url)
    if thumbnail_url is not None:
        embed.set_thumbnail(url=thumbnail_url)
    if author_name is not None:
        if author_url is not None:
            if author_icon_url is not None:
                embed.set_author(name=author_name,url=author_url,icon_url=author_icon_url)
            else:
                embed.set_author(name=author_name,url=author_url,icon_url="https://cdn.discordapp.com/attachments/559589355228889098/576422301659299860/DM_Bot.png")
        else:
            if author_icon_url is not None:
                embed.set_author(name=author_name,icon_url=author_icon_url)
            else:
                embed.set_author(name=author_name,icon_url="https://cdn.discordapp.com/attachments/559589355228889098/576422301659299860/DM_Bot.png")
    else:
        if author_url is not None:
            if author_icon_url is not None:
                embed.set_author(name="DM Bot",url=author_url,icon_url=author_icon_url)
            else:
                embed.set_author(name="DM Bot",url=author_url,icon_url="https://cdn.discordapp.com/attachments/559589355228889098/576422301659299860/DM_Bot.png")
        else:
            if author_icon_url is not None:
                embed.set_author(name="DM Bot",icon_url=author_icon_url)
            else:
                embed.set_author(name="DM Bot",icon_url="https://cdn.discordapp.com/attachments/559589355228889098/576422301659299860/DM_Bot.png")
    if fields is None:
        return embed
    else:
        for i in fields:
            embed.add_field(name=i["name"],value=i["value"],inline=i["inline"])
        else:
            return embed
