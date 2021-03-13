#!/usr/bin/python
import sys
import os
from modules.control.cmd_utils import findAllPumlaFiles

def identifyMe():
    print("pumla v0.1 - by Dr. Markus Voss")


def parseSysArg(sysarg):
    # no parameter - default behaviour: show all pumla files in subdirs
    if (len(sysarg) == 1):
        print("all pumla files in subdirs:")
        pfls = findAllPumlaFiles(os.path.curdir)
        for e in pfls:
            print(e)


if __name__ == "__main__":
    identifyMe()
    parseSysArg(sys.argv)