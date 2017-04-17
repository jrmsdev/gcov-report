import sys
import html
from os import path
from glob import glob
from . import config, parser, output, version


def __scan_files ():
    db = list()
    scan_patt = None
    if config.gcovdir == '.':
        scan_patt = '*.gcov'
    else:
        scan_patt = "{}/*.gcov".format (config.gcovdir)
    gcov_files = sorted (glob (scan_patt))
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
    print ("{} [-V|--version] [-h|--help] [options]".format (appname))
    print ("Options:")
    print ("  --htmldir={}".format (config.htmldir))


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

    def getarg(a, key, default = None):
        if a.startswith (key):
            v = a.replace (key, '', 1).strip ()
            if v == "":
                flags_invalid.append (a)
            else:
                return v
        return default

    for a in argv[1:]:

        if a == '--version' or a == '-V':
            flags['printv'] = True

        elif a == '--help' or a == '-h':
            flags['help'] = True

        elif a == '--test-mode':
            config.test_mode = True

        elif a.startswith ('--htmldir='):
            config.htmldir = getarg (a, '--htmldir=', config.DEFAULT_HTMLDIR)

        elif a.startswith ('--gcovdir='):
            config.gcovdir = getarg (a, '--gcovdir=', config.DEFAULT_GCOVDIR)

        else:
            flags_invalid.append (a)

    if len (flags_invalid) > 0:
        __usage (appname)
        print ("Invalid args:")
        for a in flags_invalid:
            print ("  '%s'" % a)
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
