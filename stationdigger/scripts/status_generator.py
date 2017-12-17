#!/usr/bin/env python
#
# Copyright 2011 Alex Dementsov
#
# Script which aggregates data for languages and genres for plotting
#


import json

INPUT_G         = "../station_genre.json"
OUTPUT_G_KEY    = "../status_genre.txt"
OUTPUT_G_VALUE  = "../status_genre_sort.txt"
INPUT_L         = "../station_lang.json"
OUTPUT_L_KEY    = "../status_lang.txt"
OUTPUT_L_VALUE  = "../status_lang_sort.txt"


def dump(filename, ls):
    if not isinstance(filename, basestring) or not isinstance(ls, list):
        return

    s   = ""
    for l in ls:
        s   += "%s %s\n" % (l[0], l[1])
    open(filename, "w").write(s)


def status_generator(input_file, key_file, value_file):
    resource   = json.loads(open(input_file).read())
    if not isinstance(resource, dict):
        return

    table    = {}
    for k, v in resource.iteritems():
        table[v["name"]] = len(v["stations"])

    items = table.items()
    
    # sorted by key
    ls  = list(items)   # list copy
    ls.sort()
    dump(key_file, ls)

    # sorted by value
    ls2 = list(items)
    ls_sorted   = sorted(ls2, key=lambda item: item[1], reverse=True)
    dump(value_file, ls_sorted)


if __name__ == "__main__":
    status_generator(INPUT_G, OUTPUT_G_KEY, OUTPUT_L_VALUE)