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

from datetime import datetime
import os
import exifread
from pybar import show_progress

######## SETTINGS ################################################################################

MAX_TIME_SPAN_IN_DAYS = 2
MAX_ALBUM_LENGTH_IN_DAYS = 14
MIN_PICS_FOR_ALBUM_SUBDIR_THRESHOLD = 10
MIN_PICS_FOR_DAY_SUBDIR_THRESHOLD = 5
PIC_FORMAT = "%Y%m%d_%H%M%S"
DIR_FORMAT = "%Y-%m-%d"

######## PICTURE CLASS ###########################################################################

class Picture(object):
    def __init__(self, file, created):
        self.__path = os.path.dirname(file)
        self.__name = os.path.basename(file)
        self.__created = created

    def get_path(self):
        return self.__path


    def set_path(self, value):
        self.__path = value

    def get_name(self):
        return self.__name


    def get_created(self):
        return self.__created


    def set_name(self, value):
        self.__name = value


    def set_created(self, value):
        self.__created = value


    def del_name(self):
        del self.__name


    def del_created(self):
        del self.__created

    def del_path(self):
        del self.__path

    path = property(get_path, set_path, del_path, "path's docstring")
    name = property(get_name, set_name, del_name, "filename as string")
    created = property(get_created, set_created, del_created, "EXIF Image Date as datetime.date")

    def rename(self):
        date_str = self.created.strftime(PIC_FORMAT)
        new_name = date_str + ".jpg"
        if self.name == new_name:
            return  # nothing do to
        if os.path.exists(os.path.join(self.path, new_name)):
            i = 0
            while True:
                i += 1
                alt_name = "{0}_{1}.jpg".format(date_str, i)
                if not os.path.exists(os.path.join(self.path, alt_name)):
                    break
            new_name = alt_name
        try:
            os.rename(os.path.join(self.path, self.name), os.path.join(self.path, new_name))
            self.name = new_name
        except OSError as error:
            print("OSError on rename '{0}' to '{1}': {2}".format(self.name, new_name, error))

    def move(self, new_path):
        try:
            os.rename(os.path.join(self.path, self.name), os.path.join(new_path, self.name))
            self.path = new_path
        except OSError as error:
            print("OSError on move '{0}' to '{1}': {2}".format(os.path.join(self.path, self.name), os.path.join(new_path, self.name), error))

    def __eq__(self, value):
        if isinstance(value, Picture):
            return self.created == value.created
        else:
            return NotImplemented

    def __gt__(self, value):
        if isinstance(value, Picture):
            return self.created > value.created
        else:
            return NotImplemented

    def __ge__(self, value):
        if isinstance(value, Picture):
            return self.created >= value.created
        else:
            return NotImplemented

    def __ne__(self, value):
        if isinstance(value, Picture):
            return self.created != value.created
        else:
            return NotImplemented

    def __lt__(self, value):
        if isinstance(value, Picture):
            return self.created < value.created
        else:
            return NotImplemented

    def ___le__(self, value):
        if isinstance(value, Picture):
            return self.created <= value.created
        else:
            return NotImplemented

######## ALBUM CLASS ###########################################################################

class Album(object):
    def __init__(self, path):
        self.__path = path
        self.__pictures = []

    def get_path(self):
        return self.__path


    def get_pictures(self):
        return self.__pictures


    def set_path(self, value):
        self.__path = value


    def set_pictures(self, value):
        self.__pictures = value


    def del_path(self):
        del self.__path


    def del_pictures(self):
        del self.__pictures

    path = property(get_path, set_path, del_path, "path's docstring")
    pictures = property(get_pictures, set_pictures, del_pictures, "pictures's docstring")

    def __len__(self):
        return len(self.__pictures)

    def add(self, picture):
        if len(self.pictures) == 0:
            self.pictures.append(picture)
            return True
        delta_to_last = picture.created - self.pictures[-1].created
        if delta_to_last.days > MAX_TIME_SPAN_IN_DAYS:            
            return False
        delta_to_first= picture.created - self.pictures[0].created    
        if delta_to_first.days > MAX_ALBUM_LENGTH_IN_DAYS:
            return False 
        else:
            self.pictures.append(picture)
            return True

    def create_subdirs(self):
        if len(self.pictures) < MIN_PICS_FOR_ALBUM_SUBDIR_THRESHOLD:
            return
        if self.pictures[0] == self.pictures[-1]:
            name = str(self.pictures[0].created.strftime(DIR_FORMAT))
        else:
            name = str(self.pictures[0].created.strftime(DIR_FORMAT)) + "_-_" + str(self.pictures[-1].created.strftime(DIR_FORMAT))
        new_path = os.path.join(self.__path, str(name))
        try:
            os.makedirs(new_path, exist_ok=True)
        except OSError as error:
            print("OSError on mkdir '{0}': {1}".format(new_path, error))
            return
        for pic in self.pictures:
            pic.move(new_path)

###################################################################################################
# PICTURE FUCTIONS
###################################################################################################

def group_pictures_by_day(pictures):
    label = "grouping pictures by DateTimeOriginal"
    pic_dict = dict()
    for pic in pictures:
        key = pic.created.strftime("%Y-%m-%d")
        if key in pic_dict:
            pic_dict[key].append(pic)
        else:
            pic_dict[key] = [pic]
    i = 0
    for date_str, pic_list in pic_dict.items():
        i += 1
        show_progress(i, len(pic_dict.items()), label)
        if len(pic_list) >= MIN_PICS_FOR_DAY_SUBDIR_THRESHOLD:
            new_path = os.path.join(pic_list[0].path, date_str)
            os.makedirs(new_path, exist_ok=True)
            for pic in pic_list:
                pic.move(new_path)

###################################################################################################

def read_pictures(filenames):
    pictures = []
    i = 0
    for filename in filenames:
        i += 1
        show_progress(i, len(filenames), "reading EXIF information")
        try:
            with open(filename, "rb") as fp:
                tags = exifread.process_file(fp, details=False, stop_tag="EXIF DateTimeOriginal")
                if "EXIF DateTimeOriginal" not in tags:
                    print("Missing EXIF metadata in file '%s'" % filename)
                    continue
                tag_value = tags["EXIF DateTimeOriginal"]
                created = datetime.strptime(str(tag_value), "%Y:%m:%d %H:%M:%S")
                pictures.append(Picture(filename, created))
        except IOError as error:
            print("IOError on '{0}' : {1}".format(filename, error))
    return pictures