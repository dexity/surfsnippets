#!/usr/bin/env python
#
# Copyright 2011 Alex Dementsov
#
# Scripts for converting stations by language to stations by genre
#

import json

GENRES  = "../generated/genres.json"
INPUT   = "../station_lang.json"
OUTPUT  = "../station_genre.json"

def lang2genre():
    langs   = json.loads(open(INPUT).read())
    genrejs = json.loads(open(GENRES).read())   # Format: {"genre_id": "genre_name"}
    genres  = {}

    for lk, lv in langs.iteritems():
        #if not lv.has_key("stations") or not :
        #    continue
        for st_id, st_val in lv["stations"].iteritems():
            add_station(genres, st_id, st_val, lk, genrejs)

    open(OUTPUT, "w").write(json.dumps(genres))  # write to file


def add_station(genres, st_id, st_val, lang_id, genrejs):
    gcode   = st_val["genre"]
    # No genre or gcode is not in the genrejs dictionary - ignore it
    if not gcode or not (isinstance(genrejs, dict) and genrejs.has_key(gcode)):
        return

    if not genres.has_key(gcode):   # make sure that genre is dictionary
        genres[gcode]   = {}

    genre   = genres[gcode]
    genre["name"]       = genrejs[gcode]    # genre name
    if not genre.has_key("stations"):
        genre["stations"]   = {}

    stations    = genre["stations"]
    station     = {
        "name":         st_val.get("name"),
        "description":  st_val.get("description"),
        "url":          st_val.get("url"),
        "image":        st_val.get("image"),
        "lang":         lang_id
    }
    stations[st_id]  = station


if __name__ == "__main__":
    lang2genre()

