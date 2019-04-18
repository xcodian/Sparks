import sqlite3
import json
import time

from debug import cOut

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sqlite3.connect("guild_data.db")
db.row_factory = dict_factory
cur = db.cursor()

def load_config():
    try:
        f = open("config.json", "r")
        return json.load(f)
    except:
        cOut("Creating/Repairing configuration file...")

        model = {"token": "ENTER TOKEN HERE",
                 "deafult_prefix": "$",
                 "description": "ENTER DESCRIPTION HERE"}

        f = open("config.json", "w+")
        json.dump(model, f, indent=4)

        print("*** PLEASE EDIT YOUR TOKEN IN THE NEWLY GENERATED config.json FILE BEFORE STARTING! ***")
        time.sleep(10)
        exit(1)

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
    cur.execute("INSERT INTO gconfig VALUES ('{}', '{}', 'N/A', 'N/A', 'N/A')".format(sid, conf['deafult_prefix']))
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
