# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(cog)
        except commands.ExtensionNotFound:
            return await ctx.send(":x: No such cog found.")
        except commands.NoEntryPointError:
            return await ctx.send(":x: Cog has no setup function.")
        except commands.ExtensionFailed:
            return await ctx.send(":x: Cog's setup function failed.")
        else:
            return await ctx.send(":white_check_mark: Successfully loaded {}".format(cog))

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        try:
            self.bot.reload_extension(cog)
        except commands.ExtensionNotFound:
            return await ctx.send(":x: Cog not found.")
        except commands.ExtensionNotLoaded:
            return await ctx.send(":x: Cog was never loaded.")
        except commands.NoEntryPointError:
            return await ctx.send(":x: Cog has no setup function.")
        except commands.ExtensionFailed:
            return await ctx.send(":x: Cog's setup function failed.")
        else:
            return await ctx.send(":white_check_mark: Successfully reloaded {}".format(cog))

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
        except commands.ExtensionNotFound:
            return await ctx.send(":x: Cog not found.")
        except commands.ExtensionNotLoaded:
            return await ctx.send(":x: Cog was never loaded.")
        else:
            return await ctx.send(":white_check_mark: Successfully unloaded {}".format(cog))


def setup(bot):
    bot.add_cog(Owner(bot))
