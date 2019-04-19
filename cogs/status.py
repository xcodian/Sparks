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
        uptime = int(time.time() - self.bot.startTime)

        embed.description = "Uptime: {} seconds".format(uptime)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))
