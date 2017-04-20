from sys import stderr

DEBUG = False

def log(*args):
    if DEBUG:
        print ("D:", *args, file = stderr)
