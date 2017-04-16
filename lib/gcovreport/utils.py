import time
from . import config

def asctime ():
    if config.test_mode:
        return "TEST_MODE:utils.asctime"
    return time.asctime ()
