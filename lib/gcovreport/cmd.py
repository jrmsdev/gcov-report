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

    for src in sorted (glob ('*.gcov')):
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
