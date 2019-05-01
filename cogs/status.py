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

        uptime = time.time() - self.bot.startTime
        clock = [
            str(time.gmtime(uptime)[2] - 1),
            str(time.gmtime(uptime)[3]),
            str(time.gmtime(uptime)[4]),
            str(time.gmtime(uptime)[5]),
        ]

        embed.add_field(
            name="Uptime", value="``{0[0]}`` days, ``{0[1]}`` hours, ``{0[2]}`` minutes, ``{0[3]}`` seconds".format(clock)
        )
        embed.set_author(name="Sparks", url="https://github.com/xxcodianxx/Sparks")
        await ctx.send(embed=embed)

    @commands.command(brief = "Invite the bot to your server.")
    async def invite(self, ctx):
        await ctx.send("<{}>".format(discord.utils.oauth_url(self.bot.user.id, discord.Permissions(permissions=2146958583))))

def setup(bot):
    bot.add_cog(Status(bot))
