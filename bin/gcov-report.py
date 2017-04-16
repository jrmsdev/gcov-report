#!/usr/bin/env python3

import sys
from os import path

lib_check = path.join (path.dirname (__file__),
        '..', 'lib', 'gcovreport', '__init__.py')

if path.isfile (lib_check):
    sys.path.insert (0, path.dirname (path.dirname (lib_check)))
    from gcovreport import cmd
else:
    try:
        from gcovreport import cmd
    except ImportError:
        print ("ERR: could not import gcovreport python lib", file = sys.stderr)
        sys.exit (1)

sys.exit (cmd.main ())
