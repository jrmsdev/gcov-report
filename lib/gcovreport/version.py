from . import config

VMAJOR = 0
VMINOR = 6
VPATCH = 1

def get_string ():
    global VPATCH
    s = "{:d}.{:d}".format (VMAJOR, VMINOR)
    if VPATCH > 0:
        s += ".{:d}".format (VPATCH)
    if config.test_mode:
        s = "TEST_MODE:version.get_string"
    return s

def project_url ():
    url = "https://gitlab.com/jrms/gcov-report"
    if config.test_mode:
        url = "TEST_MODE:version.project_url"
    return url
