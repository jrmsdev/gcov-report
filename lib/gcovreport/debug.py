from sys import stderr
from os import getenv

DEBUG = False if getenv ('GCOV_REPORT_DEBUG', None) is None else True

def log(*args):
    if DEBUG:
        print ("D:", *args, file = stderr)
