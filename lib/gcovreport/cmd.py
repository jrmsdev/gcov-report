import sys
import html
from os import path
from glob import glob
from . import config, parser, output


def __scan_files ():
    db = list()

    def gcov_append (src, gcov):
        db.append ({
            'src': html.escape (src.replace ('.gcov', '')),
            'data': gcov,
        })

    gcov_files = sorted (glob ('*.gcov'))
    if len (gcov_files) < 1:
        print ("no .gcov files were found")
        sys.exit (1)

    for src in gcov_files:
        gcov_append (src, parser.parse_gcov (src))

    return db


def __pre_checks ():
    if not path.isdir (config.htmldir):
        print (config.htmldir, "html dir not found")
        sys.exit (1)

def main ():
    __pre_checks ()
    gcovdb = __scan_files ()
    output.write_index (gcovdb)
    return 0
