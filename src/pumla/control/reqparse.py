"""The pumla command line tool functions for requirements parsing."""

import json
import os
import yaml
from pathlib import Path
from pumla.control.cmd_utils import isInBlacklist, readBlacklist


def parsePUMLAReqFile(file):
    """ parse the PUMLA Requirements file and read it
        into a dictionary."""
    reqsdict = yaml.safe_load(Path(file).read_text())
    return reqsdict


def findAllPUMLAReqFiles(path):
    """" find all pumla files in given path """
    pumlareqfiles = []
    blacklist = []

    blacklistfilename = path + "/pumla_blacklist.txt"

    blacklist = readBlacklist(path, blacklistfilename)

    # walk through the file and folder structure
    # and put all PUMLA req files into a list
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            if not isInBlacklist(dirpath, blacklist):
                #print(dirpath)
                fname = os.path.join(dirpath, filename)
                # a PUMLA req. file must end with '.yml' (see Modelling Guideline)
                if fname.endswith('.yaml'):
                    with open(fname) as myfile:
                        line = myfile.read()
                        # a PUMLA file must have that first comment line (see Modelling Guideline)
                        if line.startswith("#PUMLARR"):
                            pumlareqfiles.append(fname)

    #return the list of PUMLA req files found
    return pumlareqfiles

def updatePUMLAReqRepo(path, mrefilename):
    """create, update/overwrite the PUMLA requirements repository json file
        with current state of the source code repository"""
    # traverse down the path and find all
    # pumla req. files.
    pumlareqfiles = findAllPUMLAReqFiles(path)

    # parse each pumla file and create
    # a PUMLA Elements, Connections and
    # relations out of it, that
    # get put into dict.
    pumlareqslist = []

    # table to create the bi-directional traceability
    derived_table = []

    # sum up information from all files in common list
    for f in pumlareqfiles:
        reqs = parsePUMLAReqFile(f)
        for r in reqs:
            r.update({"derived_to": []})
            r.update({"in_file": f})
            if not r.get("derived_from")==None:
                derived_table.append({"from": r["derived_from"], "to":  r.get("alias")})
            pumlareqslist.append(r)
    # update the "derived to" attribute corresponding to the "derived from"
    for e in derived_table:
        for r in pumlareqslist:
            if r.get("alias") in e.get("from"):
                der_to = r.get("derived_to")
                der_to.append(e.get("to"))
                r.update({"derived_to": der_to})

    for r in pumlareqslist:
        if r.get("derived_from")==None:
            r["derived_from"] = []

    # make it accessible from within PlantUML.
    # $allreqs is the preprocessor variable that
    # allows access by PlantUML pumla marcros.
    pumlareqdict = {"reqsrepopath": os.path.abspath(path), "reqsrepofile": mrefilename, "reqs": pumlareqslist}
    reqjsontxt = json.dumps(pumlareqdict)
    jsontxt = "!$allreqs = " + reqjsontxt

    pumltxt = "@startjson\n" + reqjsontxt + "\n@endjson\n"
    pumltxtlines = pumltxt.split("},")

    # split text to make the resulting file more readable;
    # one element definition per line.
    txt_lines = jsontxt.split("},")

    # write the lines to the model element repo file
    with open(mrefilename, "w") as fil:
        for i in range(len(txt_lines) - 1):
            fil.write(txt_lines[i] + "},\n")
        fil.write(txt_lines[len(txt_lines) - 1] + "\n\n")
    fil.close()

    # write the lines to the model element repo file
    with open("reqs_json_diagram.puml", "w") as fil:
        for i in range(len(pumltxtlines) - 1):
            fil.write(pumltxtlines[i] + "},\n")
        fil.write(pumltxtlines[len(pumltxtlines) - 1] + "\n\n")
    fil.close()

    return True, mrefilename, pumlareqslist


