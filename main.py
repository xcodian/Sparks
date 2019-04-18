# -*- coding: utf-8 -*-

import argparse
import json
import os
import subprocess
import sys
from json import JSONDecodeError
from subprocess import CalledProcessError

from bot import Sparks

os.chdir(sys.path[0])


def is_venv():
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def main(reset=False):
    try:
        with open("config.json") as f:
            config = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        with open("config.json", "w") as f:
            f.write("{}")

        with open("config.json") as f:
            config = json.load(f)

    if config.get("token") is None or reset is True:
        config["token"] = input("Enter a bot token: ")

    if config.get("description") is None:
        config["description"] = input("Enter a bot description: ")

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    arguments = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    if not is_venv():
        arguments.insert(4, "--user")

    try:
        subprocess.check_call(" ".join(arguments), shell=True)
    except CalledProcessError:
        print("Dependency installation failed.")
        input("Press Enter to exit.")
        raise SystemExit()
    Sparks()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", "-r", action="store_true")
    args = parser.parse_args()

    if args.reset:
        main(reset=True)
    else:
        main()
