import discord
from discord.ext import commands


class botStatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", brief="Get the connection latency.")
    async def ping(self, ctx):
        embed = discord.Embed(title="", description=":stopwatch: {}ms".format(int(self.bot.latency * 1000)), color=discord.Color.blurple())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(botStatusCog(bot))