import discord
from discord.ext import commands
from util import error, flagParse

import traceback
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    async def mainMenu(self, ctx, command_list : list, cursor_pos : int):
        embed = discord.Embed(
            colour = discord.Color.blurple(),
            title = "Bot Commands",
            description="``Use the arrows to navigate the list``"
        )

        for idx, command in enumerate(command_list):
            short_desc = str(command.brief) or "No Information Provided."
            command_name = "**[ {} ]**".format(command.name.capitalize()) if idx == cursor_pos else command.name.capitalize()

            embed.add_field(name = command_name, value = short_desc, inline = False)

        return embed

    async def commandEntry(self, ctx, command : commands.Command):
        embed = discord.Embed(
            colour = discord.Color.blurple(),
            title = "Command: {}".format(command.name.capitalize()),
        )

        embed.description = "```{}{} {}```\n".format(ctx.prefix, command.name, command.usage or "")
        embed.description += "{}".format(command.description or command.brief or "No Information Provided.")

        return embed

    async def waitForAction(self, ctx, message, nav : dict, timeout = 60):
        def check(reaction, user):
            return (str(reaction.emoji) in nav.keys()) and (user == ctx.author) and (reaction.message.id == message.id)

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout = timeout, check = check)
        except asyncio.TimeoutError:
            return asyncio.TimeoutError, None, None

        return nav[str(reaction)], reaction, user


    @commands.command(
        description="""
        *Displays information about commands that can be executed through the bot. \n``command`` parameter can be left blank to view all commands.*
        
        **Parameters**
        ``[command]`` | Command to get help about, can be left blank.
        ``-showhidden`` | Flag that shows all of the bot commands, even hidden ones.

        """,
        usage = "[command]  [-showhidden]",
        brief = "View help for bot commands."
    )
    async def help(self, ctx, help_object = None):

        # 'await' expressions in comprehensions are not supported in Python 3.5, considering upgrade?
        cmdlist = []
        for command in sorted(self.bot.commands, key = lambda x: x.name):
            if await command.can_run(ctx):
                cmdlist.append(command)

        cursor = 0
        page = "main"

        if help_object is None:
            help_message = await ctx.send(embed = await self.mainMenu(ctx, cmdlist, cursor))

        else:
            if help_object not in [command.name for command in cmdlist]:
                raise commands.BadArgument("Command '{}' does not exist.".format(help_object))

            elif not self.bot.get_command(help_object).can_run(ctx):
                await ctx.send(embed=error("You cannot view help for this command as you lack the permissions to execute it."))
                return

            else:
                help_message = await ctx.send(embed = await self.commandEntry(ctx, self.bot.get_command(help_object)))

        def cursor_down():
            nonlocal cursor
            if cursor + 1 < len(cmdlist):
                cursor += 1

        def cursor_up():
            nonlocal cursor
            if cursor - 1 > -1:
                cursor -= 1

        def view_mainmenu():
            nonlocal page
            page = "main"

        def view_command():
            nonlocal page
            page = cmdlist[cursor]

        navpanel = {
            "⬆": cursor_up,
            "⬇": cursor_down,
            "⬅": view_mainmenu,
            "➡": view_command
        }

        for emoji in ["⬅", "⬆", "⬇", "➡"]:
            await help_message.add_reaction(emoji)

        while True:
            control_callback, reaction, user = await self.waitForAction(ctx, help_message, navpanel)
            if control_callback == asyncio.TimeoutError:
                break

            control_callback()
            await help_message.remove_reaction(reaction, user)

            embed = None
            if page == "main":
                embed = await self.mainMenu(ctx, cmdlist, cursor)

            elif isinstance(page, commands.Command):
                embed = await self.commandEntry(ctx, page)

            if embed is None:
                break

            await help_message.edit(embed=embed)

        # End
        embed = help_message.embeds[0]
        embed.colour = discord.Color.dark_grey()

        await help_message.edit(embed=embed)
        await help_message.clear_reactions()

def setup(bot):
    bot.add_cog(Help(bot))
