#!/usr/bin/python

class CS:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    YELLOW = '\u001b[33m'
    CYAN = '\u001b[36m'
    MAGENTA = '\u001b[35m'

    def print_warning(msg):
        print(CS.WARNING + msg + CS.ENDC)

    def print_blue(msg):
        print(CS.OKBLUE + msg + CS.ENDC)

    def print_green(msg):
        print(CS.OKGREEN + msg + CS.ENDC)

    def print_fail(msg):
        print(CS.FAIL + msg + CS.ENDC)

    def print_header(msg):
        print(CS.HEADER + msg + CS.ENDC)

    def print_high(msg):
        print(CS.YELLOW + msg + CS.ENDC)
