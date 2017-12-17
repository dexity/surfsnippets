#!/usr/bin/env python
#
# Copyright 2011 Alex Dementsov
#
# Scripts for merging files with stations by a single language into one file
#

import os
import re
import json

JSFILE  = "lang([\d]+).json"

def merge_langs():
    dirname = "../stations"
    ld      = os.listdir(dirname)
    langs   = {}

    for file in ld:
        p   = re.compile(JSFILE)
        m   = p.findall(file)
        if len(m) != 1:
            continue

        filename    = "%s/%s" % (dirname, file)
        lang        = json.loads(open(filename).read())
        for k, v in lang.iteritems():
            langs[k]    = v

    open("station_lang.json", "w").write(json.dumps(langs))

    
if __name__ == "__main__":
    merge_langs()
