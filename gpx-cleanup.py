#!/usr/bin/env python3

import os
import gpxpy
import gpxpy.gpx


for dirname in os.listdir("tracks"):
    full_dirname = os.path.join("tracks", dirname)
    for filename in os.listdir(full_dirname):
        print(filename)
        f = os.path.join(full_dirname, filename)
        fh = open(f, 'r')
        gpx = gpxpy.parse(fh)
        fh.close()
        gpx.creator = 'gpx.py -- https://github.com/tkrajina/gpxpy'
        gpx.link = None
        gpx.time = None
        gpx.author_name = None
        gpx.name = filename[0:-4]
        gpx.extensions = []
        gpx.metadata_extensions = []
        for t in gpx.tracks:
            t.name = None
            t.type = None
            t.description = None
        fh = open(f, 'w')
        fh.write(gpx.to_xml())
        fh.close()

