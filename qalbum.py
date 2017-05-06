#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# This file is part of qalbum (picture renaming script).
#
# qalbum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qalbum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qalbum.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2017, Nico Rittstieg

import os
import sys
from easygui import diropenbox
from pictures import Album
from pictures import group_pictures_by_day
from pictures import read_pictures
from pybar import show_progress

###################################################################################################

def main():
    path = diropenbox("Choose a photo directory" , "Quick Album")
    if path == None:
        sys.exit(0)
    filenames = scan_files(path)
    print("Found %d pictures in '%s'" % (len(filenames), path))
    pictures = read_pictures(filenames)
    # sort pictures by creation date
    pictures.sort()
    # rename files?
    if input("Rename pictures by EXIF DateTimeOriginal? [y/n]: ").lower() == "y":
        i = 0;
        for pic in pictures:
            i += 1
            show_progress(i, len(pictures), "renaming files")
            pic.rename()
    # create album objects
    albums = create_albums(path, pictures)
    # create a subdirs for each album?
    if input("Create subdirs for photo albums? [y/n]: ").lower() == "y":
        i = 0;
        for album in albums:
            i += 1
            show_progress(i, len(albums), "creating subdirs for albums")
            album.create_subdirs()
    # create a subdir for each day?
    if input("Group pictures by image date? [y/n]: ").lower() == "y":
        group_pictures_by_day(pictures)
    input("Press <ENTER> to quit...")

###################################################################################################

def scan_files(path):
    filenames = []
    for entry in os.scandir(path):
        if entry.is_file():
            filename = entry.name.lower()
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                filenames.append(os.path.join(path, entry.name))
    return filenames

###################################################################################################

def create_albums(path, pictures):
    albums = []
    album = None
    for picture in pictures:
        if album == None or album.add(picture) == False:
            album = Album(path)
            albums.append(album)
            album.add(picture)
    return albums

###################################################################################################

if __name__ == '__main__':
    main()
