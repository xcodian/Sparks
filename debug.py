# -*- coding: utf-8 -*-

import discord
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
                return Exception("Unexpected argument '{}'".format(i))

            else:
                # add it as an arg to the flag it belongs to
                output[belongsto].append(i)
                # fulfill the demand
                demand -= 1

    if demand > 0:  # if there is still demand
        return Exception("Not enough arguments supplied.")

    return output


def error(text: str):
    return discord.Embed(description="{}".format(text), colour=0xE06C75)

def embedOut(text: str):
    return discord.Embed(description="{}".format(text), colour=discord.Colour.blue())
