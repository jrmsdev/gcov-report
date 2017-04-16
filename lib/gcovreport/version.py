from . import config

VMAJOR = 0
VMINOR = 3
VPATCH = 0

def get_string ():
    if config.test_mode:
        return "TEST_MODE:version.get_string"
    v = "%d.%d" % (VMAJOR, VMINOR)
    if VPATCH > 0:
        v += ".%d" % VPATCH
    return v

def printv (appname = 'gcov-report'):
    print ("%s v%s" % (appname, get_string ()))

def project_url ():
    if config.test_mode:
        return "TEST_MODE:version.project_url"
    return "https://github.com/jrmsdev/gcov-report"
