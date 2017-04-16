import sys
import html
from os import path
from glob import glob
from . import config, parser, output, version


def __scan_files ():
    db = list()

    gcov_files = sorted (glob ('*.gcov'))
    if len (gcov_files) < 1: # pragma: no cover
        print ("no .gcov files were found")
        sys.exit (1)

    for src in gcov_files:
        db.append (parser.parse_gcov (src))

    return db


def __pre_checks ():
    if not path.isdir (config.htmldir): # pragma: no cover
        print (config.htmldir, "html dir not found")
        sys.exit (1)


def __usage (appname): # pragma: no cover
    print ("%s [-V|--version] [-h|--help]" % appname)


def __parse_argv (argv):
    appname = path.basename (argv[0])
    argc = len (argv)
    if argc == 1: # pragma: no cover
        return
    flags_invalid = list()
    flags = {
        'printv': False,
        'help': False,
    }
    for a in argv[1:]:
        if a == '--version' or a == '-V':
            flags['printv'] = True
        elif a == '--help' or a == '-h':
            flags['help'] = True
        elif a == '--test-mode':
            config.test_mode = True
        else:
            flags_invalid.append (a)
    if len (flags_invalid) > 0:
        __usage (appname)
        print ("invalid args:")
        for a in flags_invalid:
            print (" ", a)
        sys.exit (3)
    if flags['printv']:
        version.printv (appname = appname)
        sys.exit (0)
    elif flags['help']:
        __usage (appname)
        sys.exit (0)


def main ():
    __parse_argv (sys.argv)
    __pre_checks ()
    gcovdb = __scan_files ()
    output.write_index (gcovdb)
    return 0
