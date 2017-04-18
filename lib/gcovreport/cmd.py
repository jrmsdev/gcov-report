import sys
import html
from os import path
from glob import glob
from getopt import getopt, GetoptError

from . import config, parser, output, version

__cmdopts = [
    # options name format as in help(getops) documentation
    {
        'long': 'version', 'short': 'V',
        'default': None,
        'help': 'show version and exit',
    },
    {
        'long': 'help', 'short': 'h',
        'default': None,
        'help': 'show this help message',
    },
    {
        'long': 'htmldir=', 'short': 'o:',
        'default': config.DEFAULT_HTMLDIR,
        'help': 'html/output directory path',
    },
    {
        'long': 'gcovdir=', 'short': 'i:',
        'default': config.DEFAULT_GCOVDIR,
        'help': 'input directory path containing *.gcov files to parse',
    },
]


def main ():
    cmdname = path.basename (sys.argv[0])

    def usage ():
        print ("{} [-h|-V] [options]".format (cmdname))
        print ()
        print ("Options (", version.get_string (), "):", sep = '')

        for opt in __cmdopts:
            print ("  ", end = '') # indent

            if opt['short'] is not None:
                print ("-{}".format (opt['short'].replace (':', '')), end = '')
                if opt['long'] is not None:
                    print(", ", end = '')

            if opt['long'] is not None:
                print ("--", opt['long'], sep = '', end = '')
                if opt['default'] is not None:
                    print ("'", opt['default'], "' *", sep = '', end = '')

            if opt['help'] is not None:
                print ()
                print ("      ", opt['help'], sep = '', end = '')
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
                if opt['long'] is not None:
                    longopts.append (opt['long'])
                if opt['short'] is not None:
                    shortopts += str (opt['short'])
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
            print (opt)
            optn = opt[0]
            optv = opt[1]

            if optn == '--version' or optn == '-V':
                flags['version'] = True

            elif optn == '--help' or optn == '-h':
                flags['help'] = True

            elif optn == '--test-mode':
                config.test_mode = True

            elif optn.startswith ('--htmldir='):
                config.htmldir = optv or config.DEFAULT_HTMLDIR

            elif optn.startswith ('--gcovdir='):
                config.gcovdir = optv or config.DEFAULT_GCOVDIR

        if flags['version']:
            print (version.get_string (cmdname))
            sys.exit (0)

        elif flags['help']:
            usage ()
            sys.exit (0)

        sys.exit (128)

    def pre_checks ():
        if not path.isdir (config.htmldir):
            print (config.htmldir, "html dir not found")
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
    gcovdb = scan_files ()
    output.write_index (gcovdb)

    return 0
