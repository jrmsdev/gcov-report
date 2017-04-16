import sys
import html
from os import path
from glob import glob
from . import config, parser, output, version


def __scan_files ():
    db = list()

    gcov_files = sorted (glob ('*.gcov'))
    if len (gcov_files) < 1:
        print ("no .gcov files were found")
        sys.exit (1)

    for src in gcov_files:
        db.append (parser.parse_gcov (src))

    return db


def __pre_checks ():
    if not path.isdir (config.htmldir):
        print (config.htmldir, "html dir not found")
        sys.exit (1)


def __usage (appname):
    print ("%s [-V|--version] [-h|--help]" % appname)


def __parse_argv (argv):
    appname = path.basename (argv[0])
    argc = len (argv)
    if argc == 1:
        return
    if argc > 2:
        print ("invalid args number")
        __usage (appname)
        sys.exit (1)
    for a in argv[0:]:
        if a == '--version' or a == '-V':
            version.printv (appname = appname)
            sys.exit (0)
        elif a == '--help' or a == '-h':
            __usage (appname)
            sys.exit (0)
    print ("invalid arg")
    __usage (appname)
    sys.exit (3)


def main ():
    __parse_argv (sys.argv)
    __pre_checks ()
    gcovdb = __scan_files ()
    output.write_index (gcovdb)
    return 0
