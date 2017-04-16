VMAJOR = 0
VMINOR = 0
VPATCH = 0

def get_string ():
    v = "%d.%d" % (VMAJOR, VMINOR)
    if VPATCH > 0:
        v += ".%d" % VPATCH
    return v

def printv (appname = 'gcov-report'):
    print ("%s v%s" % (appname, get_string ()))
