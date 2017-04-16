VMAJOR = 0
VMINOR = 1
VPATCH = 0

def get ():
    v = "%d.%d" % (VMAJOR, VMINOR)
    if VPATCH > 0:
        v += ".%d" % VPATCH
    return v

def printv ():
    print ("gcov-report v%s" % get ())
