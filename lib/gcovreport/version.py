from . import config

VMAJOR = 0
VMINOR = 4
VPATCH = 0

def get_string ():
    if not config.test_mode: # pragma: no cover
        v = "%d.%d" % (VMAJOR, VMINOR)
        if VPATCH > 0:
            v += ".%d" % VPATCH
        return v
    return "TEST_MODE:version.get_string"

def printv (appname = 'gcov-report'): # pragma: no cover
    print ("%s v%s" % (appname, get_string ()))

def project_url ():
    if not config.test_mode: # pragma: no cover
        return "https://gitlab.com/jrms/gcov-report"
    return "TEST_MODE:version.project_url"
