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
__version__ = "0.8.2"
__maintainer__ = "Dr. Markus Voss (private person)"
__status__ = "Development"

import argparse
import os
from pumla.control.cmd_utils import findAllPUMLAFiles, parsePUMLAFile, updatePUMLAMR, createPumlaMacrosFile

parser = None
parser_getjson = None

def identifyMe(parser):
    """ information about the executed command """
    print(parser.description)


def cmdInit(args):
    print("initialisng source code repository for pumla usage...")
    mypath_main = main.__code__.co_filename
    pumla_module_path = mypath_main.replace("src/pumla/main.py", "")
    createPumlaMacrosFile(pumla_module_path)
    print("done.")

def cmdCreateNewPumlaFile(args):
    pass

def cmdListElements(args):
    print("\nPUMLA elements:\n")
    # pfls = list of PUMLA files
    pfls = findAllPUMLAFiles(os.path.curdir)

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
    (success, efn, a, b, c) = updatePUMLAMR(os.path.curdir, args.mrefilename)
    if success:
        print("model repo file: " + efn)
        print("done.")
    else:
        print("failed.")


def cmdListFiles(args):
    identifyMe(parser)
    print("all pumla files in subdirs:")
    pfls = findAllPUMLAFiles(os.path.curdir)
    for e in pfls:
        print(e)

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

    parser_update = subparsers.add_parser(
        "update",
        help="(re-)generate `modelrepo_json.puml` with updated info from `pumla` model elements found in repository.",
    )
    parser_update.add_argument(
        "mrefilename",
        help="filename for model repo JSON file",
        nargs="?",
        default=os.path.curdir + "/modelrepo_json.puml",
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


