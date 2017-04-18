from . import config

VMAJOR = 0
VMINOR = 5
VPATCH = 0

def get_string (cmdname = 'gcov-report'):
    s = cmdname
    if not config.test_mode: # pragma: no cover
        s += " v{:d}.{:d}".format (VMAJOR, VMINOR)
        if VPATCH > 0:
            s += ".{:d}".format (VPATCH)
        return s
    return s + " TEST_MODE:version.get_string"

def project_url ():
    if not config.test_mode: # pragma: no cover
        return "https://gitlab.com/jrms/gcov-report"
    return "TEST_MODE:version.project_url"
