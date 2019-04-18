# -*- coding: utf-8 -*-

import json
import os
import sys
def launch():
    if sys.version_info[0] < 3:
        print("Python version 3 or higher required.")
        input("Press enter to exit.")
        raise SystemExit()
      
    try:
        import discord
        from discord.ext import commands
        import sqlite3
    except ImportError as e:
        print("Dependency error: {}".format(e))
        input("Press enter to exit.")
        raise SystemExit()
 
    try:
        with open("config.json") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("config.json", "w") as f:
            model = {"token": "", "default_prefix": "$", "description": ""}

            json.dump(model, f, indent=4)

        with open("config.json") as f:
            config = json.load(f)

        print("Please enter configuration parameters.")

    if config["token"] is "":
        config["token"] = input("TOKEN: ")

    if config["description"] is "":
        config["description"] = input("DESCRIPTION: ")

    with open("config.json", "w+") as f:
        json.dump(config, f, indent=4)

    from bot import Sparks

    Sparks()


if __name__ == "__main__":
    launch()
