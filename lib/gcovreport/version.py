from os import path
from . import config

VMAJOR = 0
VMINOR = 7
VPATCH = 0

def __string ():
    s = "{:d}.{:d}".format (VMAJOR, VMINOR)
    if VPATCH > 0:
        s += ".{:d}".format (VPATCH)
    if config.test_mode:
        s = "TEST_MODE:version.get_string"
    return s

def __release ():
    f = path.join (path.realpath (path.dirname (__file__)), 'release.txt')
    try:
        with open (f, 'r') as fh:
            l = fh.readline().strip()
            fh.close()
        return l.split()
    except OSError:
        pass
    return ('', '', '')

def get_string ():
    s = __string ()
    r = __release ()
    try:
        if r[2] != '':
            if r[1] == "v{}".format (s):
                s += " ({:.7s})".format (r[2])
    except IndexError:
        pass
    return s

def project_url ():
    url = "https://gitlab.com/jrms/gcov-report"
    if config.test_mode:
        url = "TEST_MODE:version.project_url"
    return url
