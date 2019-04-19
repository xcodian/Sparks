# -*- coding: utf-8 -*-

import time

import discord
from discord.ext import commands


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Get the connection latency.")
    async def ping(self, ctx):
        embed = discord.Embed(
            description=":stopwatch: {}ms".format(int(self.bot.latency * 1000)), colour=discord.Colour.blurple()
        )
        await ctx.send(embed=embed)

    @commands.command(brief="Get some info about the bot.")
    async def info(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.description = "A Discord bot created using [discord.py](https://github.com/Rapptz/discord.py)"

        clock = [str(time.localtime()[2]), str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]

        uptime = []
        for c, o in zip(clock, self.bot.startTime):
            uptime.append(int(c) - int(o))

        embed.add_field(name="Uptime", value="{0[0]} days, {0[1]} hours, {0[2]} minutes, {0[3]} seconds".format(uptime))
        embed.set_author(name="Sparks", url="https://github.com/xxcodianxx/Sparks")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))
