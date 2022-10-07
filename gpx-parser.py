#!/usr/bin/env python3

import os
import gpxpy
import gpxpy.gpx

def write_header(f):
    f.write("""

function onZoomEnd(e) {
    level = e.target.getZoom();
    var opacity;
    if(level > 11)
        opacity = 1.0;
    else
        opacity = 0.0;
    for (let i = 0; i < markers.length; i++) {
        markers[i].setOpacity(opacity);
    }
}

var map = L.map('map').setView([48.636993, 9.008789], 13);

map.on('zoomend', onZoomEnd);
    
map = map.locate({setView: true, maxZoom: 13});

var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var latlngs;
var marker;
var markers = [];
var track;
var tracks = [];
""")

def write_track(fh, track, color, filename, fullname):
    fh.write("latlngs = [\n")
    for point in track:
        fh.write(F"[{point[0]},{point[1]}],")
    fh.write("];\n")
    popup = F"<a href=\\\"{fullname}\\\" type=\\\"application/gpx+xm\\\" download>{filename[:-4]}</a>"
    fh.write(F"""
track = L.polyline(latlngs, {{color: '{color}', interactive: 'true'}}).addTo(map);
tracks.push(track);
marker = L.marker([{track[0][0]}, {track[0][1]}]).addTo(map);
marker.bindPopup(\"{popup}\");
markers.push(marker);
""")



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
            write_track(fh, track, color, filename, f)

fh.close()

