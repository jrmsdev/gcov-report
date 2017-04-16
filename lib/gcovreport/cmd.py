import sys
from os import path

from . import config

def __pre_checks ():
    if not path.isdir (config.htmldir):
        print (config.htmldir, "html dir not found")
        sys.exit (1)

def main ():
    __pre_checks ()
    return 0
