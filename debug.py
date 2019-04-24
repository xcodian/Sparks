# -*- coding: utf-8 -*-

import discord
import asyncio
from discord.ext import commands


def cOut(msg):
    import time

    clock = [str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]

    for idx, i in enumerate(clock):
        clock[idx] = "0" * (2 - len(i)) + i if len(i) < 2 else i

    h, m, s = clock
    print("[{}:{}:{}] > {}".format(h, m, s, msg))


def end(text="Press enter to exit."):
    input(text)
    return SystemExit


def flagParse(txt, acc_flags):
    output = {}
    demand = 0
    belongsto = None

    txt = txt.lstrip(" ").rstrip(" ")

    if txt == "":
        return {}

    for i in txt.split(" "):
        if (i in acc_flags) and demand == 0:
            demand = acc_flags[i]  # get the demand of args for that flag
            output[i] = []
            belongsto = i  # mark any following ARGS as belonging to this flag

            # we don't wanna accept that one again
            del acc_flags[i]

        else:
            # is arg
            if demand == 0:  # exceeds accepted args for the flag; no demand
                return commands.BadArgument

            else:
                # add it as an arg to the flag it belongs to
                output[belongsto].append(i)
                # fulfill the demand
                demand -= 1

    if demand > 0:  # if there is still demand
        return commands.MissingRequiredArgument

    return output


def error(text: str):
    return discord.Embed(description="{}".format(text), colour=0xE06C75)


def embedOut(text: str):
    return discord.Embed(description="{}".format(text), colour=discord.Colour.green())


async def survey(bot, ctx, timeout=10):
    try:

        def check(m):
            return ctx.author == m.author

        msg = await bot.wait_for("message", timeout=timeout, check=check)
        return msg
    except asyncio.TimeoutError:
        return asyncio.TimeoutError


def set_maintenance(bot, value):
    bot.maintenance = value
    return ":unlock: Bot open to public." if not bot.maintenance else ":lock: Bot closed for maintenance."
