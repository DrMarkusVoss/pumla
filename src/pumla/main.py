#!/usr/bin/python
#
# Original pumla source code developed by Dr. Markus Voss in 2021.
# Original pumla repository:
# https://github.com/DrMarkusVoss/pumla
#
"""Command Line Tool for the PlantUML extension to enable architecture
element re-usability.
"""

__author__ = "Dr. Markus Voss (private person)"
__copyright__ = "(C) Copyright 2021 by Dr. Markus Voss (private person)"
__license__ = "GPL"
__version__ = "1.1.1"
__maintainer__ = "Dr. Markus Voss (private person)"
__status__ = "Development"

import argparse
import os
from pumla.control.cmd_utils import findAllPUMLAFiles, parsePUMLAFile, updatePUMLAMR
from pumla.control.cmd_utils import createPumlaMacrosFile, createPumlaBlacklistFile
from pumla.control.cmd_utils import createPumlaProjectConfigFile, pumlaSetup, pumlaVersionCheck
from pumla.control.cmd_utils import checkElsRelsConsForAliasExistence
from pumla.control.cmd_utils import installPlantUMLJAR
from pumla.control.cmd_utils import gendiagram
from pumla.control.cmd_utils import genpumladiag
from pumla.control.reqparse import updatePUMLAReqRepo

parser = None
parser_getjson = None

def identifyMe(parser):
    """ information about the executed command """
    print(parser.description)

def getPumlaInstallationPath():
    '''return the path to the python pumla CLI tool installation.'''
    pipath = ""

    mypath_main = main.__code__.co_filename.replace(os.sep, '/')

    # this is the case for a 'pip install -e .' case
    if ("src/pumla/main.py" in mypath_main):
        pipath = mypath_main.replace("src/pumla/main.py", "")
    # this is the case for a 'pip install .' case
    elif ("site-packages/pumla/main.py" in mypath_main):
        pipath = mypath_main.replace("main.py", "")
    # if we're here, we have a problem because of unforeseen installation circumstances...
    else:
        print("pumla error: Could not determine pumla installation path.\nPlease raise a bug-ticket at: https://github.com/DrMarkusVoss/pumla")

    return pipath

def cmdInit(args):
    '''initialise a source code repository that contains pumla architecture
       documentation for use on a new system. E.g. deal with different
       installation pathes of the source code repo and the pumla
       installation.'''
    identifyMe(parser)
    print("initialising source code repository for pumla usage...")
    success = createPumlaMacrosFile(getPumlaInstallationPath())
    if success:
        print("done.")
    else:
        print("failed.")


def cmdSetup(args):
    '''setup this computer for usage of pumla. Therefore, the python CLI
       tool needs to be connected with the pumla PlantUML macros.
       Therefore a file at CLI binary location needs to be placed that
       refers to the path of the pumla PlantUML macros.'''
    identifyMe(parser)
    print("setup pumla for usage on this machine...")

    versionsOK = pumlaVersionCheck(getPumlaInstallationPath(), __version__)

    if versionsOK:
        pumlaSetup(getPumlaInstallationPath())
        print("done.")
    else:
        print("failed.")

def cmdCheckSetup(args):
    '''check the setup and installation of pumla python CLI tool and
       pumla macros as well as path setup on this machine.'''
    identifyMe(parser)
    print("checking pumla installation on this machine...")

    versionsOK = pumlaVersionCheck(getPumlaInstallationPath(), __version__)

    if versionsOK:
        print("pumla setup is OK.")
        print("done.")
    else:
        print("failed.")

def cmdSetupPrj(args):
    '''setup a source code repository to use pumla as architecture
       documentation tool. E.g. create a pumla_blacklist.txt and a
       pumla_project_config.puml, and calls init step afterwards.'''
    identifyMe(parser)
    print("Setup project repository for pumla usage...")
    createPumlaBlacklistFile()
    pcfsuccess = createPumlaProjectConfigFile(getPumlaInstallationPath())
    print("initialising source code repository for pumla usage...")
    pmfsuccess = createPumlaMacrosFile(getPumlaInstallationPath())
    if pcfsuccess and pmfsuccess:
        print("done.")
    else:
        print("failed.")


def cmdInstallPlantUML(args):
    '''download the PlantUML JAR library and put it into a directory
       under the pumla command line tool installation.'''
    identifyMe(parser)
    print("Installing PlantUML JAR file:")
    pumpath = getPumlaInstallationPath()
    ipj_success = installPlantUMLJAR(pumpath)

    if ipj_success:
        print("done.")
    else:
        print("failed.")


def cmdGenDiagram(args):
    identifyMe(parser)
    print("Generating a diagram picture file for a PlantUML or pumla file.")
    pumpath = getPumlaInstallationPath()
    gendiagram(pumpath, args.inputfile, ".", args.picformat)

def cmdGenPumlaDiag(args):
    identifyMe(parser)
    print("Generating a pumla layout diagram .svg file for a pumla diagram file.")
    pumpath = getPumlaInstallationPath()
    genpumladiag(pumpath, args.inputfile, ".", args.layoutoverride)

def cmdCreateNewPumlaFile(args):
    pass

def cmdListElements(args):
    identifyMe(parser)
    print("\nPUMLA elements:\n")
    # pfls = list of PUMLA files
    pfls, diagfls = findAllPUMLAFiles(os.path.curdir)

    # pelems = list of PUMLA elements
    pelems = []

    # parse each PUMLA file
    # and fill PUMLA elements list
    for fn in pfls:
        # pel = PUMLA element
        (pels, rels, cons, tvs) = parsePUMLAFile(fn)
        for pel in pels:
            pelems.append(pel)

    # print out the details of each
    # element of the PUMLA elements list
    for e in pelems:
        e.printMe()
        print("")


def cmdUpdate(args):
    """create/update/overwrite the pumla model repository"""
    identifyMe(parser)
    print("updating...")
    (success_mr, efn, a, b, c) = updatePUMLAMR(os.path.curdir, args.mrefilename)
    (success_rr, rfn, reqslist) = updatePUMLAReqRepo(os.path.curdir, args.rrefilename)

    if success_mr:
        print("model repo file: " + efn)
        print("done.")
    else:
        print("failed.")

    if success_rr:
        print("reqs repo file: " + rfn)
        print("done.")
    else:
        print("failed.")

def cmdCheckAlias(args):
    """check whether a given alias name is already used in the
    current model repository"""
    print("checking model repository for occurrence of alias name: ", args.aliasnametocheck)

    alias_already_existing = False

    #identifyMe(parser)
    print("first updating model repository...")
    (success, efn, elements, relations, connections) = updatePUMLAMR(os.path.curdir, os.path.curdir + "/modelrepo_json.puml")
    if success:
        print("model repo file: " + efn)
        print("done.")
        alias_already_existing = checkElsRelsConsForAliasExistence(elements, relations, connections, args.aliasnametocheck)
        if not alias_already_existing:
            print("alias '" + args.aliasnametocheck + "' can be used as an alias or id for a new element, relation or connection.")
    else:
        print("checking failed due to update failure.")


def cmdListFiles(args):
    identifyMe(parser)
    print("all pumla files in subdirs:")
    pfls, diagfls = findAllPUMLAFiles(os.path.curdir)
    print("elements:")
    for e in pfls:
        print(e)

    print("\ndiagrams:")
    for d in diagfls:
        print(d)

def getJSONElementsCLI(args):
    """ print out a list of all model elements of the repo to the command line """
    (success, efn, jsonelems, jsonrels, jsoncons) = updatePUMLAMR(os.path.curdir, args.mrefilename)
    if success:
        print(jsonelems)
    else:
        # silent command line output if failed
        print("")

def getJSONRelationsCLI(args):
    """ print out a list of all model relations of the repo to the command line """
    (success, efn, jsonelems, jsonrels, jsoncons) = updatePUMLAMR(os.path.curdir, args.mrefilename)
    if success:
        print(jsonrels)
    else:
        # silent command line output if failed
        print("")

def getJSONConnectionsCLI(args):
    """ print out a list of all model connections of the repo to the command line """
    (success, efn, jsonelems, jsonrels, jsoncons) = updatePUMLAMR(os.path.curdir, args.mrefilename)
    if success:
        print(jsoncons)
    else:
        # silent command line output if failed
        print("")

def getJSON(args):
    identifyMe(parser)
    print("")
    parser_getjson.print_help()

def main():
    """ parses and executes the given command line arguments """
    global parser
    global parser_getjson

    parser = argparse.ArgumentParser(
        description=f"pumla v{__version__} - by {__author__}",
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v' + __version__)

    subparsers = parser.add_subparsers(
        title="available commands",
        metavar="",
        help="One of these commands must be used in order to execute pumla functionality:",
    )

    parser_init = subparsers.add_parser(
        "init",
        help="initialise a source code folder as root for a pumla model repository.",
    )
    parser_init.set_defaults(func=cmdInit)

    parser_setup = subparsers.add_parser(
        "setup",
        help="setup pumla for usage on this machine. Must be called from root folder "
             "of a cloned pumla repo or a downloaded release archive after pumla has been "
             "installed with pip.",
    )
    parser_setup.set_defaults(func=cmdSetup)

    parser_checksetup = subparsers.add_parser(
        "checksetup",
        help="check whether the current installation of pumla python CLI tool is consistent"
             "with the pumla macros file and the paths are setup all right.",
    )
    parser_checksetup.set_defaults(func=cmdCheckSetup)

    parser_installplantuml = subparsers.add_parser(
        "installplantuml",
        help="downloads the PlantUML JAR file and puts it into a dedicated directory within the"
             "pumla command line tool installation."
    )
    parser_installplantuml.set_defaults(func=cmdInstallPlantUML)

    parser_gendiagram = subparsers.add_parser(
        "gendiagram",
        help="generates a .png file for the given PlantUML or pumla file. "
    )
    parser_gendiagram.add_argument(
        "inputfile",
        help="the PlantUML or pumla file to process."
    )
    parser_gendiagram.add_argument(
        "picformat",
        help="the format of the output picture file. Default='png', others available 'txt' and 'svg'.",
        nargs="?",
        default="png",
    )
    parser_gendiagram.set_defaults(func=cmdGenDiagram)

    parser_genpumladiag = subparsers.add_parser(
        "genpumladiag",
        help="generates a diagram in .svg file format for the given PlantUML diagram file using the pumla layout engine. "
    )
    parser_genpumladiag.add_argument(
        "inputfile",
        help="the pumla diagram file to process."
    )
    parser_genpumladiag.add_argument(
        "layoutoverride",
        help="options to override the layout defaults or settings'.",
        nargs="?",
        default="none",
    )
    parser_genpumladiag.set_defaults(func=cmdGenPumlaDiag)

    parser_setupprj = subparsers.add_parser(
        "setupprj",
        help="create an environment to use pumla as architecture documentation tool in the current project repository.",
    )
    parser_setupprj.set_defaults(func=cmdSetupPrj)

    parser_listelements = subparsers.add_parser(
        "elements",
        help="list all `pumla` model elements of the model repository repository.",
    )
    parser_listelements.set_defaults(func=cmdListElements)

    parser_listfiles = subparsers.add_parser(
        "files",
        help="list all `pumla` marked model files of the model repository.",
    )
    parser_listfiles.set_defaults(func=cmdListFiles)

    parser_checkalias = subparsers.add_parser(
        "checkalias",
        help="checks whether a give alias name is already used in the current model repository.",
    )

    parser_checkalias.add_argument(
        "aliasnametocheck",
        help="the alias name to check whether it can be used for a new element."
    )

    parser_checkalias.set_defaults(func=cmdCheckAlias)

    parser_update = subparsers.add_parser(
        "update",
        help="(re-)generate `modelrepo_json.puml` and `reqsrepo_json.puml` "
             "with updated info from `pumla` model elements found in repository.",
    )
    parser_update.add_argument(
        "mrefilename",
        help="filename for model repo JSON file",
        nargs="?",
        default=os.path.curdir + "/modelrepo_json.puml",
    )
    parser_update.add_argument(
        "rrefilename",
        help="filename for reqs repo JSON file",
        nargs="?",
        default=os.path.curdir + "/reqsrepo_json.puml",
    )
    parser_update.set_defaults(func=cmdUpdate)

    parser_getjson = subparsers.add_parser(
        "getjson",
        help="get a JSON-formatted list of the requested elements on the command line, relations or "
             "connections. Call 'pumla getjson -h' \
             for help on the available subcommands.",
    )
    parser_getjson.set_defaults(func=getJSON)

    parser_getjsonsubparser = parser_getjson.add_subparsers(
        title = "available sub-commands",
        metavar="",
        help="",
    )

    parser_getjson_elements = parser_getjsonsubparser.add_parser(
        "elements",
        help="get a JSON list of all elements of the model repo on the command line.",
    )
    parser_getjson_elements.add_argument(
        "mrefilename",
        help="filename for model repo JSON file",
        nargs="?",
        default=os.path.curdir + "/modelrepo_json.puml",
    )
    parser_getjson_elements.set_defaults(func=getJSONElementsCLI)

    parser_getjson_relations = parser_getjsonsubparser.add_parser(
        "relations",
        help="get a JSON list of all relations of the model repo on the command line.",
    )
    parser_getjson_relations.add_argument(
        "mrefilename",
        help="filename for model repo JSON file",
        nargs="?",
        default=os.path.curdir + "/modelrepo_json.puml",
    )
    parser_getjson_relations.set_defaults(func=getJSONRelationsCLI)

    parser_getjson_connections = parser_getjsonsubparser.add_parser(
        "connections",
        help="get a JSON list of all connections of the model repo on the command line.",
    )
    parser_getjson_connections.add_argument(
        "mrefilename",
        help="filename for model repo JSON file",
        nargs="?",
        default=os.path.curdir + "/modelrepo_json.puml",
    )
    parser_getjson_connections.set_defaults(func=getJSONConnectionsCLI)

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError as ae:
        # no parameter - default behaviour: show help
        parser.print_help()


