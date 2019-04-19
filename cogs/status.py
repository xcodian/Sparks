# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import time

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Get the connection latency.")
    async def ping(self, ctx):
        embed = discord.Embed(
            description=":stopwatch: {}ms".format(int(self.bot.latency * 1000)), color=discord.Colour.blurple()
        )
        await ctx.send(embed=embed)

    @commands.command(name="info", brief="Get some info about the bot.")
    async def info(self, ctx):
        embed = discord.Embed(color=discord.Color.blurple())

        uptime = int(time.time() - self.bot.startTime)
        embed.add_field(name=":clock2: **Uptime:**".format(uptime), value="``{}s``")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Status(bot))
