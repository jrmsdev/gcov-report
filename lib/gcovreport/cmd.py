import sys
import html
from os import path
from glob import glob
from getopt import getopt, GetoptError

from . import config, version, debug, htmlx
from .gcov import parser


class CmdOption:
    long = None
    short = None
    default = None
    help = None

    def __init__ (self, long = None, short = None, default = None, help = None):
        self.long = long
        self.short = short
        self.default = default
        self.help = help



__cmdopts = [
    # options name format as in help(getops) documentation
    CmdOption (
        long = 'help', short = 'h',
        default = None,
        help = 'show this help message',
    ),
    CmdOption (
        long = 'version', short = 'V',
        default = None,
        help = 'show version and exit',
    ),
    CmdOption (
        long = 'gcovdir=', short = 'i:',
        default = config.DEFAULT_GCOVDIR,
        help = 'input directory path containing *.gcov files to parse',
    ),
    CmdOption (
        long = 'htmldir=', short = 'o:',
        default = config.DEFAULT_HTMLDIR,
        help = 'html/output directory path',
    ),
    # hidden option (only used for internal tests)
    CmdOption (
        long = 'test-mode', short = None,
        default = None,
        help = None,
    ),
]


def main ():
    cmdname = path.basename (sys.argv[0])

    def usage ():
        print (cmdname, " v", version.get_string (), "", sep = '')
        print ()
        print ("{} [-h|-V] [options]".format (cmdname))

        for opt in __cmdopts:
            if opt.help is None:
                continue

            print ("  ", end = '') # indent

            if opt.short is not None:
                print ("-{}".format (opt.short.replace (':', '')), end = '')
                if opt.long is not None:
                    print(", ", end = '')

            if opt.long is not None:
                print ("--", opt.long, sep = '', end = '')
                if opt.default is not None:
                    print ("'", opt.default, "' *", sep = '', end = '')

            if opt.help is not None:
                print ()
                print ("      ", opt.help, sep = '', end = '')
            print ()

        print ()
        print ("* an option arg is required (show default values)")
        print ()

    def parse_argv ():
        if len (sys.argv[1:]) == 0:
            return

        flags = {
            'version': False,
            'help': False,
        }

        def getopts_and_args ():
            shortopts = ""
            longopts = list ()
            for opt in __cmdopts:
                if opt.long is not None:
                    longopts.append (opt.long)
                if opt.short is not None:
                    shortopts += str (opt.short)
            return getopt (sys.argv[1:], shortopts, longopts)

        try:
            opts, args = getopts_and_args ()
        except GetoptError as err:
            # option not recognized
            usage ()
            print (str (err))
            sys.exit (1)

        if len (args) > 0:
            usage ()
            print ("command arg(s) not recognized:",
                " ".join(["'{}'".format(a) for a in args]))
            sys.exit (1)

        for opt in opts:
            optn = opt[0]
            optv = opt[1]

            if optn == '--version' or optn == '-V':
                flags['version'] = True

            elif optn == '--help' or optn == '-h':
                flags['help'] = True

            elif optn == '--test-mode':
                config.test_mode = True

            elif optn == '--gcovdir' or optn == '-i':
                config.gcovdir = optv or config.DEFAULT_GCOVDIR

            elif optn == '--htmldir' or optn == '-o':
                config.htmldir = optv or config.DEFAULT_HTMLDIR

        # -- test mode enabled
        if config.test_mode:
            print (cmdname, "test mode enabled")

        # -- debug mode enabled
        if debug.DEBUG:
            debug.log (cmdname, "debug mode enabled")

        # -- print version and exit
        if flags['version']:
            print (cmdname, " v", version.get_string (), sep = '')
            sys.exit (0)

        # -- print help and exit
        elif flags['help']:
            usage ()
            sys.exit (0)

    def pre_checks ():
        if not path.isdir (config.htmldir):
            err = "{}: htmldir not found".format (config.htmldir)
            if config.test_mode:
                err = err.replace (config.htmldir, path.basename (config.htmldir), 1)
            print (err)
            sys.exit (1)

    def scan_files ():
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

    parse_argv ()
    pre_checks ()

    debug.log ("htmldir:", config.htmldir)
    debug.log ("gcovdir:", config.gcovdir)

    gcovdb = scan_files ()
    htmlx.output.write_index (gcovdb)

    return 0
