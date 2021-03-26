#!/usr/bin/python
import sys
import os
from modules.control.cmd_utils import findAllPUMLAFiles, parsePUMLAFile, updatePUMLAMR

def identifyMe():
    """ information about the executed command """
    print("pumla v0.2 - by Dr. Markus Voss")

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
                pel = parsePUMLAFile(fn)
                pelems.append(pel)

            # print out the details of each
            # element of the PUMLA elements list
            for e in pelems:
                e.printMe()
                print("")

        elif (sysarg[1] == "update"):
            print("updating...")
            if (len(sysarg) > 2):
                mrfilename = sysarg[2]
            else:
                # setup the filename to store the JSON model repo
                mrfilename = os.path.curdir + "/mrtest_json.puml"
            # create/update/overwrite the pumla model repository
            (success, fn) = updatePUMLAMR(os.path.curdir, mrfilename)
            if (success):
                print("file: " + fn)
                print("done.")
            else:
                print("failed.")


if __name__ == "__main__":
    identifyMe()
    parseSysArg(sys.argv)