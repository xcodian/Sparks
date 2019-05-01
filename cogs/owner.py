# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import asyncio

import util
from util import cOut
import botdata as bd


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        brief = "Manage the bot maintenance mode.",

        description = """
                *Bot maintenance disallows the bot to be used by any users other than the bot owners.*
                *You can use this command to enable, disable and view the status of maintenance mode.*
                
                **Parameters**
                ``[action]`` | Action to perform. Leave blank to view status.
                
                **Actions**
                ``enable``  | Enables maintenance mode.
                ``disable`` | Disables maintenance mode.
                ``toggle``  | Toggles maintenance mode.
                """,
        usage = "[action]",
        hidden = True
    )
    async def maintenance(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                embed=util.embedOut(
                    "The bot is currently in maintenance mode."
                    if self.bot.maintenance
                    else "The bot is currently out of maintenance mode."
                )
            )

    @maintenance.command(hidden=True)
    @commands.check(util.is_bot_admin)
    async def enable(self, ctx):
        msg = util.set_maintenance(self.bot, True)
        await ctx.send(embed=util.embedOut(msg))

    @maintenance.command(hidden=True)
    @commands.check(util.is_bot_admin)
    async def disable(self, ctx):
        msg = util.set_maintenance(self.bot, False)
        await ctx.send(embed=util.embedOut(msg))

    @maintenance.command(hidden=True)
    @commands.check(util.is_bot_admin)
    async def toggle(self, ctx):
        if self.bot.maintenance:
            msg = util.set_maintenance(self.bot, False)
        else:
            msg = util.set_maintenance(self.bot, True)
        await ctx.send(embed=util.embedOut(msg))

    @commands.command(
        brief = "Rebuild the database.",

        description = """
                *The guild database contains configuration data for all servers the bot is part of.*
                *This command can rebuild the database and add any servers that have been left out.*
                
                **Parameters**
                ``-all`` | Use with this flag to rebuild ALL guilds the bot is in. Leave blank to rebuild the current server.
                
                :information_source: This command may require aditional confirmation.
                
                :warning: It is not recommended to execute any other commands while this is running.
                """,
        usage = "[-all]",
        hidden = True
    )
    @commands.check(util.is_bot_admin)
    async def rebuild(self, ctx, *, args=""):
        f = util.flagParse(args, {"-all": 0})

        if f == commands.MissingRequiredArgument:
            raise commands.MissingRequiredArgument

        elif f == commands.BadArgument:
            raise commands.BadArgument

        if "-all" in f:
            await ctx.send("```Are you sure that you want to rebuild data records for ALL guilds? (y/N)```")
            response = await util.survey(self.bot, ctx)

            if response != asyncio.TimeoutError and response.content.lower() == "y":
                await ctx.send(embed=util.embedOut(util.set_maintenance(self.bot, True)))

                msg = await ctx.send(embed=util.embedOut("Rebuilding database..."))
                bd.rebuild_all(self.bot.guilds)
                await msg.edit(
                    embed=util.embedOut(":white_check_mark: Rebuilt database for ``{}`` guilds.".format(len(self.bot.guilds)))
                )

                await ctx.send(embed=util.embedOut(util.set_maintenance(self.bot, False)))

            else:
                await ctx.send(embed=util.error("Operation aborted."))
        else:
            await ctx.send(embed=util.embedOut(util.set_maintenance(self.bot, True)))

            bd.rebuild_one(ctx.guild.id)
            await ctx.send(embed=util.embedOut(":white_check_mark: Rebuilt database for local guild."))
            await ctx.send(embed=util.embedOut(util.set_maintenance(self.bot, False)))

    @commands.check(util.is_bot_admin)
    @commands.command(brief="Run as another user.", hidden=True, usage="<user>")
    async def sudo(self, ctx, user:discord.Member, *, cmd):
        sudo_msg = ctx.message

        if user is None:
            raise commands.BadArgument("Invalid user.")

        sudo_msg.author = user
        sudo_msg.content = cmd

        sudo_ctx = await self.bot.get_context(sudo_msg)
        response = await self.bot.invoke(sudo_ctx)

        cOut("SUDO: User '{0}' (ID {0.id}) executed '{1}' as '{2}' (ID {2.id}). RESULT: {3}".format(ctx.author, sudo_msg.content, sudo_ctx.author, response))


def setup(bot):
    bot.add_cog(Owner(bot))
