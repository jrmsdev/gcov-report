import time
from . import config

def asctime ():
    if not config.test_mode: # pragma: no cover
        return time.asctime ()
    return "TEST_MODE:utils.asctime"
