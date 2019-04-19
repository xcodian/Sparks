# -*- coding: utf-8 -*-

import json
import sqlite3
import time

from debug import cOut, end
import bot


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect("guild_data.db")
db.row_factory = dict_factory
cur = db.cursor()


def load_config():
    with open("config.json") as f:
        return json.load(f)


conf = load_config()


def preflight_checks():
    # TODO: move this into addTable and create independence for rebuild_cols
    def rebuild_cols(table, cols):  # adds missing columns
        for col in cols:
            try:
                cur.execute("ALTER TABLE {} ADD COLUMN {}".format(table, col))
            except Exception as e:
                if isinstance(e, sqlite3.OperationalError):
                    pass

    try:
        cur.execute("CREATE TABLE gconfig (id, prefix, starboard, welcome, announcements)")

    except Exception as e:
        if isinstance(e, sqlite3.OperationalError):
            rebuild_cols("config", ["id", "prefix", "starboard", "welcome", "announcements"])

    try:
        cur.execute("CREATE TABLE gconfig (id, prefix)")
    except Exception as e:
        if isinstance(e, sqlite3.OperationalError):
            rebuild_cols("config", ["id", "prefix", "starboard", "welcome", "announcements"])


preflight_checks()


def getServer(sid):
    cur.execute("SELECT * FROM gconfig WHERE id = '{}'".format(sid))
    row = cur.fetchone()
    return row


def addServer(sid):
    cur.execute("INSERT INTO gconfig VALUES ('{}', '{}', 'N/A', 'N/A', 'N/A')".format(sid, conf["default_prefix"]))
    db.commit()
    return getServer(sid)


def delServer(sid):
    try:
        cur.execute("DELETE FROM gconfig WHERE id = {}".format(sid))
        db.commit()
        return True
    except Exception as e:
        return e


def modServer(sid, col, newvalue):
    try:
        cur.execute("UPDATE gconfig SET {} = '{}' WHERE id = '{}'".format(col, newvalue, sid))
        db.commit()
        return getServer(sid)
    except Exception as e:
        return e

def rebuild_all(guilds):
    for guild in guilds:
        rebuild_one(guild.id)

def rebuild_one(sid):
    backup = getServer(sid)
    if backup is None:
        addServer(sid)
        return True

    cur.execute("DELETE FROM gconfig WHERE id = {}".format(sid))
    db.commit()

    addServer(sid)
    for k, v in zip(backup.keys(), backup.values()):
        modServer(sid, k, v)
    return True

if __name__ == "__main__":
    raise end()
