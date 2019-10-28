import discord
from discord.ext import commands
import resource.trng as rand

class Dice(commands.Cog):

    def __init__(self,client):
        self.client = client

    # Commands
    @commands.command(aliases=["r",'dice'])
    async def roll(self, ctx, arg="1d20", arg2=None):
        add_num = 0
        kh_dice = 0
        kl_dice = 0
        arg_copy = arg.lower()

        if "-" in arg:
            plus_split = arg.split("-")
            add_num -= int(plus_split[1])
            arg_copy = plus_split[0]

        if "+" in arg:
            plus_split = arg.split("+")
            add_num += int(plus_split[1])
            arg_copy = plus_split[0]

        if "kh" in arg.lower() and "kl" in arg.lower():
            if arg_copy.find("h") < arg_copy.find("l"):
                kl_split = arg_copy.split("kl")
                kl_dice = int(kl_split[1])
                arg_copy = kl_split[0]
                kh_split = arg_copy.split("kh")
                kh_dice = int(kh_split[1])
                arg_copy = kh_split[0]
            else:
                kh_split = arg_copy.split("kh")
                kh_dice = int(kh_split[1])
                arg_copy = kh_split[0]
                kl_split = arg_copy.split("kl")
                kl_dice = int(kl_split[1])
                arg_copy = kl_split[0]

        elif "kh" in arg_copy:
            kh_split = arg_copy.split("kh")
            kh_dice = int(kh_split[1])
            arg_copy = kh_split[0]

        elif "kl" in arg_copy:
            kl_split = arg_copy.split("kl")
            kl_dice = int(kl_split[1])
            arg_copy = kl_split[0]
        

        if "d" not in arg.lower():
            await ctx.send("<@%d>,\nAdding `%s+%d`, you got\n`%s`" % (ctx.author.id,arg_copy,add_num,int(arg_copy)+add_num))
        else:
            d_split = arg_copy.split("d")

            num_of_dice = int(d_split[0])
            dice_sides = int(d_split[1])

            if kh_dice + kl_dice >= num_of_dice:
                kh_dice = 0
                kl_dice = 0

            if arg2 is not None:
                if arg2.lower() == "adv" or arg2.lower() == "advantage":

                    if [kl_dice,kh_dice] == [0,0]:
                        kh_dice = num_of_dice

                    num_of_dice *= 2

                elif arg2.lower() == "dis" or arg2.lower() == "disadvantage":

                    if [kl_dice,kh_dice] == [0,0]:
                        kl_dice = num_of_dice

                    num_of_dice *= 2

            dice_roll_count = 0
            result = []
            result_copy = []
            dice_total = 0

            while dice_roll_count < num_of_dice:
                dice_roll = rand.randbelow(1,dice_sides) + add_num
                result.append(dice_roll)
                result_copy.append(dice_roll)
                dice_total += dice_roll
                dice_roll_count += 1

            if kh_dice != 0:

                sort_result = sorted(result_copy)[kl_dice:]

                while len(sort_result) > kh_dice:
                    dice_total -= sort_result[0]
                    result[result.index(sort_result[0])] = "~~`%d`~~" % sort_result[0]
                    del sort_result[0]
                
            elif kl_dice != 0:

                sort_result = sorted(result_copy)

                while len(sort_result) > kl_dice:

                    if dice_total > sort_result[-1]:
                        dice_total -= sort_result[-1]

                    else:
                        dice_total = 0
                    result[result.index(sort_result[-1])] = "~~`%d`~~" % sort_result[-1]
                    del sort_result[-1]

            for i in result:

                if type(i) is int:

                    if i == dice_sides + add_num:
                        result[result.index(i)] = "**`%d`**" % i

                    else:
                        result[result.index(i)] = "`%d`" % i

            if len(str(result)) < 2000:
                if type(ctx.channel) == discord.TextChannel:
                    await ctx.channel.purge(limit=1)
                if arg2 is not None:
                    if arg2.lower() == "adv" or arg2.lower() == "advantage":
                        if kl_dice == 1 or kh_dice == 1:
                            await ctx.send("<@%d>,\nRolling `%s` **with advantage**, you got\n%s" % (ctx.author.id,arg,str(result).strip("[]").replace("'","")))

                        else:
                            await ctx.send("<@%d>,\nRolling `%s` **with advantage**, you got\n%s\ntotaling at `%d`" % (ctx.author.id,arg,str(result).strip("[]").replace("'",""),dice_total))


                    elif arg2.lower() == "dis" or arg2.lower() == "disadvantage":
                        if kl_dice == 1 or kh_dice == 1:
                            await ctx.send("<@%d>,\nRolling `%s` **with disadvantage**, you got\n%s" % (ctx.author.id,arg,str(result).strip("[]").replace("'","")))

                        else:
                            await ctx.send("<@%d>,\nRolling `%s` **with disadvantage**, you got\n%s\ntotaling at `%d`" % (ctx.author.id,arg,str(result).strip("[]").replace("'",""),dice_total))


                else:
                    if num_of_dice == 1 or kh_dice + kl_dice == 1:
                        await ctx.send("<@%d>,\nRolling `%s`, you got\n`%d`" % (ctx.author.id,arg,result_copy[0]))

                    else:
                        await ctx.send("<@%d>,\nRolling `%s`, you got\n%s\ntotaling at `%d`" % (ctx.author.id,arg,str(result).strip("[]").replace("'",""),dice_total))

            else:
                if type(ctx.channel) == discord.TextChannel:
                    await ctx.channel.purge(limit=1)
                await ctx.send("<@%d>, your rolls are too powerful, they reached over the 2000 character limit." % ctx.author.id)



def setup(client):
    client.add_cog(Dice(client))
