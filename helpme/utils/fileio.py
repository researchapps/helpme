"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import configparser
import errno
import os
import pwd
import re
import tempfile
import json
import io
import sys

from helpme.logger import bot

# FOLDER OPERATIONS ############################################################


def get_userhome():
    """get the user home based on the effective uid
    """
    return pwd.getpwuid(os.getuid())[5]


def mkdir_p(path):
    """mkdir_p attempts to get the same functionality as mkdir -p
    :param path: the path to create.
    """
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            bot.error("Error creating path %s, exiting." % path)
            sys.exit(1)


# CONFIG OPERATIONS ############################################################


def write_config(filename, config, mode="w"):
    """use configparser to write a config object to filename
    """
    with open(filename, mode) as filey:
        config.write(filey)
    return filename


def read_config(filename):
    """use configparser to write a config object to filename
    """
    config = configparser.ConfigParser()
    config.read(filename)
    return config


# FILE OPERATIONS ##############################################################


def generate_temporary_file(folder="/tmp", prefix="helpme", ext="json"):
    """write a temporary file, in base directory with a particular extension.
      
       Parameters
       ==========
       folder: the base directory to write in. 
       prefix: the prefix to use
       ext: the extension to use.

    """
    tmp = next(tempfile._get_candidate_names())
    return "%s/%s.%s.%s" % (folder, prefix, tmp, ext)


def copyfile(source, destination, force=True):
    """copy a file from a source to its destination.
    """
    if os.path.exists(destination) and force is True:
        os.remove(destination)
    shutil.copyfile(source, destination)
    return destination


def write_file(filename, content, mode="w"):
    """write_file will open a file, "filename" and write content, "content"
    and properly close the file
    """
    with open(filename, mode) as filey:
        filey.writelines(content)
    return filename


def write_json(json_obj, filename, mode="w", print_pretty=True):
    """write_json will (optionally,pretty print) a json object to file
    :param json_obj: the dict to print to json
    :param filename: the output file to write to
    :param pretty_print: if True, will use nicer formatting
    """
    with open(filename, mode) as filey:
        if print_pretty:
            filey.writelines(print_json(json_obj))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def print_json(json_obj):
    """ just dump the json in a "pretty print" format
    """
    return json.dumps(json_obj, indent=4, separators=(",", ": "))


def read_file(filename, mode="r", readlines=True):
    """write_file will open a file, "filename" and write content, "content"
    and properly close the file
    """
    with open(filename, mode) as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def read_json(filename, mode="r"):
    """read_json reads in a json file and returns
    the data structure as dict.
    """
    with open(filename, mode) as filey:
        data = json.load(filey)
    return data
