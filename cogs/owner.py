# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from util import cOut, error, embedOut, flagParse, survey, set_maintenance
import botdata as bd
import asyncio


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    async def maintenance(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                embed=embedOut(
                    "The bot is currently in maintenance mode."
                    if self.bot.maintenance
                    else "The bot is currently out of maintenance mode."
                )
            )

    @maintenance.command(hidden=True)
    @commands.is_owner()
    async def enable(self, ctx):
        msg = set_maintenance(self.bot, True)
        await ctx.send(embed=embedOut(msg))

    @maintenance.command(hidden=True)
    @commands.is_owner()
    async def disable(self, ctx):
        msg = set_maintenance(self.bot, False)
        await ctx.send(embed=embedOut(msg))

    @maintenance.command(hidden=True)
    @commands.is_owner()
    async def toggle(self, ctx):
        if self.bot.maintenance:
            msg = set_maintenance(self.bot, False)
        else:
            msg = set_maintenance(self.bot, True)
        await ctx.send(embed=embedOut(msg))

    @commands.command(name="rebuild", hidden=True)
    @commands.is_owner()
    async def rebuild(self, ctx, *, args=""):
        f = flagParse(args, {"-all": 0})

        if f == commands.MissingRequiredArgument:
            raise commands.MissingRequiredArgument

        elif f == commands.BadArgument:
            raise commands.BadArgument

        if "-all" in f:
            await ctx.send("```Are you sure that you want to rebuild data records for ALL guilds? (y/N)```")
            response = await survey(self.bot, ctx)

            if response != asyncio.TimeoutError and response.content.lower() == "y":
                await ctx.send(embed=embedOut(set_maintenance(self.bot, True)))

                msg = await ctx.send(embed=embedOut("Rebuilding database..."))
                bd.rebuild_all(self.bot.guilds)
                await msg.edit(
                    embed=embedOut(":white_check_mark: Rebuilt database for ``{}`` guilds.".format(len(self.bot.guilds)))
                )

                await ctx.send(embed=embedOut(set_maintenance(self.bot, False)))

            else:
                await ctx.send(embed=error("Operation aborted."))
        else:
            await ctx.send(embed=embedOut(set_maintenance(self.bot, True)))

            bd.rebuild_one(ctx.guild.id)
            await ctx.send(embed=embedOut(":white_check_mark: Rebuilt database for local guild."))
            await ctx.send(embed=embedOut(set_maintenance(self.bot, False)))

    @commands.is_owner()
    @commands.command(brief="Run as another user.", hidden=True)
    async def sudo(self, ctx, user, *, cmd):
        sudo_msg = ctx.message
        try:
            sudo_msg.author = ctx.guild.get_member(int(user.replace("<@", "").replace(">", "")))
        except:
            sudo_msg.author = None

        if sudo_msg.author is None:
            raise commands.BadArgument("user")

        sudo_msg.content = cmd

        sudo_ctx = await self.bot.get_context(sudo_msg)
        await self.bot.invoke(sudo_ctx)


def setup(bot):
    bot.add_cog(Owner(bot))
