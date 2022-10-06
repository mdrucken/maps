#!/usr/bin/env python3

import os
import gpxpy
import gpxpy.gpx

def write_header(f):
    f.write("""

function onTrackClick(e) {
    if(e.target.options.opacity > 0.5)
        e.target.setStyle({opacity: "0.3"});
    else
        e.target.setStyle({opacity: "1.0"});
    e.target.redraw();
}

var map = L.map('map').setView([48.636993, 9.008789], 13);
    
map = map.locate({setView: true, maxZoom: 13});

var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var latlngs;
""")

def write_track(fh, track, color, filename):
    fh.write("latlngs = [\n")
    for point in track:
        fh.write("[{},{}],".format(point[0], point[1]))
    fh.write("];\n")
    fh.write("var polyline = L.polyline(latlngs, {color: '" + color + "', interactive: 'true'}).addTo(map);\n")
    fh.write("polyline.on('click', onTrackClick);")
    fh.write("polyline.bindTooltip(\"{}\");".format(filename))



def get_track(f):
    fh = open(f, 'r')
    gpx = gpxpy.parse(fh)
    ret = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                ret.append([point.latitude, point.longitude])
    fh.close()
    return ret



fh = open("tracks.js", "w")
write_header(fh)

for dirname in os.listdir("tracks"):
    if dirname.upper().find("RADTOUR") >= 0:
        pass
    else:
        print(dirname)
        full_dirname = os.path.join("tracks", dirname)
        color = ""
        if dirname.upper().find("TODO") == 0:
            color = "red"
        elif dirname.upper().find("UNSORTED") == 0:
            color = "yellow"
        else:
            color = "blue"
        for filename in os.listdir(full_dirname):
            f = os.path.join(full_dirname, filename)
            track = get_track(f)
            write_track(fh, track, color, filename)

fh.close()

