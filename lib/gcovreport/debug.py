from sys import stderr

DEBUG = True

def log(*args):
    if DEBUG:
        print ("D:", *args, file = stderr)
