# -*- coding: utf-8 -*-

import json
import os
import sys


def launch():
    if sys.version_info[0] < 3:
        print("Python version 3 or higher required.")

        # cannot use debug.end here since it may not be installed.
        input("Press enter to exit.")
        raise SystemExit()

    try:
        import discord
        from discord.ext import commands
        import sqlite3

        import util

    except ImportError as e:
        print("Dependency error: {}".format(e))

        # cannot use debug.end here since it may not be installed.
        input("Press enter to exit.")
        raise SystemExit()

    try:
        with open("config.json") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("config.json", "w") as f:
            model = {"token": "", "default_prefix": "$", "description": "", "bot_owners":[]}

            json.dump(model, f, indent=4)

        with open("config.json") as f:
            config = json.load(f)

        print("Please enter configuration parameters.")

    if config["token"] is "":
        config["token"] = input("TOKEN: ")

    if len(config["bot_owners"]) < 1:
        for i in input("BOT OWNERS (split by ','): ").replace(" ", "").split(","):
            if input("Add id '{}' as bot owner? (y/n): ".format(i)).lower() == "y":
                config["bot_owners"].append(i)
                print("Added id '{}' to bot owners list.".format(i))

            else:
                print("Skipping id '{}'.".format(i))


    with open("config.json", "w+") as f:
        json.dump(config, f, indent=4)

    from bot import Sparks

    Sparks()


if __name__ == "__main__":
    launch()
