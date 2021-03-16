#!/usr/bin/python
import sys
import os
from modules.control.cmd_utils import findAllPUMLAFiles, parsePUMLAFile

def identifyMe():
    """ information about the executed command """
    print("pumla v0.1 - by Dr. Markus Voss")

def parseSysArg(sysarg):
    """ parses the given command line arguments """
    # no parameter - default behaviour: show all pumla files in subdirs
    if (len(sysarg) == 1):
        print("all pumla files in subdirs:")
        pfls = findAllPumlaFiles(os.path.curdir)
        for e in pfls:
            print(e)
    else:
        if (sysarg[1] == "showelements"):
            print("PUMLA elements:\n")
            # pfls = list of PUMLA files
            pfls = findAllPUMLAFiles(os.path.curdir)

            # pelems = list of PUMLA elements
            pelems = []

            # parse each PUMLA file
            # and fill PUMLA elements list
            for fn in pfls:
                # pel = PUMLA element
                pel = parsePUMLAFile(fn)
                pelems.append(pel)

            # print out the details of each
            # element of the PUMLA elements list
            for e in pelems:
                e.printMe()
                print("")

if __name__ == "__main__":
    identifyMe()
    parseSysArg(sys.argv)