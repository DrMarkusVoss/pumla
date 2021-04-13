#!/usr/bin/python
import sys
import os
from modules.control.cmd_utils import findAllPUMLAFiles, parsePUMLAFile, updatePUMLAMR

def identifyMe():
    """ information about the executed command """
    print("pumla v0.4 - by Dr. Markus Voss")

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
            # if there is another command line argument after the update command...
            if (len(sysarg) > 2):
                # take 3rd command line argument as filename for model repo JSON file
                mrefilename = sysarg[2]
                mrrfilename = os.path.curdir + "/relationsrepo_json.puml"
                mrcfilename = os.path.curdir + "/connectionsrepo_json.puml"
            else:
                # setup the default filename to store the JSON model repo
                mrefilename = os.path.curdir + "/modelrepo_json.puml"
                mrrfilename = os.path.curdir + "/relationsrepo_json.puml"
                mrcfilename = os.path.curdir + "/connectionsrepo_json.puml"
            if (len(sysarg) > 3):
                mrrfilename = sysarg[2]
                mrcfilename = os.path.curdir + "/connectionsrepo_json.puml"
            if (len(sysarg) > 4):
                mrcfilename = sysarg[3]

            # create/update/overwrite the pumla model repository
            (success, efn, rfn, cfn) = updatePUMLAMR(os.path.curdir, mrefilename, mrrfilename, mrcfilename)
            if (success):
                print("element repo file: " + efn)
                print("relations repo file: " + rfn)
                print("connections repo file: " + cfn)
                print("done.")
            else:
                print("failed.")


if __name__ == "__main__":
    identifyMe()
    parseSysArg(sys.argv)