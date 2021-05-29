#!/usr/bin/python
"""Command Line Tool for the PlantUML extension to enable architecture
element re-usability.
"""

__author__ = "Dr. Markus Voss (private person)"
__copyright__ = "(C) Copyright 2021 by Dr. Markus Voss (private person)"
__license__ = "GPL"
__version__ = "0.5.1"
__maintainer__ = "Dr. Markus Voss (private person)"
__status__ = "Development"

import sys
import os
from modules.control.cmd_utils import findAllPUMLAFiles, parsePUMLAFile, updatePUMLAMR



def identifyMe():
    """ information about the executed command """
    print("pumla v0.5 - by Dr. Markus Voss")

def parseSysArg(sysarg):
    """ parses the given command line arguments """
    # no parameter - default behaviour: show all pumla files in subdirs
    if (len(sysarg) == 1):
        print("all pumla files in subdirs:")
        pfls = findAllPUMLAFiles(os.path.curdir)
        for e in pfls:
            print(e)
    else:
        if (sysarg[1] == "listelements"):
            print("\nPUMLA elements:\n")
            # pfls = list of PUMLA files
            pfls = findAllPUMLAFiles(os.path.curdir)

            # pelems = list of PUMLA elements
            pelems = []

            # parse each PUMLA file
            # and fill PUMLA elements list
            for fn in pfls:
                # pel = PUMLA element
                (pels, rels, cons) = parsePUMLAFile(fn)
                for pel in pels:
                    pelems.append(pel)

            # print out the details of each
            # element of the PUMLA elements list
            for e in pelems:
                #print(e)
                e.printMe()
                print("")

        elif (sysarg[1] == "update"):
            print("updating...")
            # if there is another command line argument after the update command...
            if (len(sysarg) > 2):
                # take 3rd command line argument as filename for model repo JSON file
                mrefilename = sysarg[2]
            else:
                # setup the default filename to store the JSON model repo
                mrefilename = os.path.curdir + "/modelrepo_json.puml"

            # create/update/overwrite the pumla model repository
            (success, efn) = updatePUMLAMR(os.path.curdir, mrefilename)
            if (success):
                print("model repo file: " + efn)
                print("done.")
            else:
                print("failed.")


if __name__ == "__main__":
    identifyMe()
    parseSysArg(sys.argv)