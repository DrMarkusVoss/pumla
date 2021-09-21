#!/usr/bin/python
"""Command Line Tool for the PlantUML extension to enable architecture
element re-usability.
"""

__author__ = "Dr. Markus Voss (private person)"
__copyright__ = "(C) Copyright 2021 by Dr. Markus Voss (private person)"
__license__ = "GPL"
__version__ = "0.8.1"
__maintainer__ = "Dr. Markus Voss (private person)"
__status__ = "Development"

import argparse
import os
from pumla.control.cmd_utils import findAllPUMLAFiles, parsePUMLAFile, updatePUMLAMR

def identifyMe(parser):
    """ information about the executed command """
    print(parser.description)


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
    print("updating...")
    (success, efn) = updatePUMLAMR(os.path.curdir, args.mrefilename)
    if success:
        print("model repo file: " + efn)
        print("done.")
    else:
        print("failed.")


def cmdListFiles(args):
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
    print("Call with one of the mandatory sub-commands, e.g.")
    print("pumla getjson elements\n")
    print("Call ")
    print("pumla getjson -h")
    print("for help.")


def main():
    """ parses and executes the given command line arguments """
    parser = argparse.ArgumentParser(
        description=f"pumla v{__version__} - by {__author__}"
    )
    subparsers = parser.add_subparsers(
        title="available commands",
        metavar="",
        help="One of these commands must be used in order to execute pumla functionality:",
    )
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
        help="get a JSON list of the requested elements, relations or connections. Call 'pumla getjson -h' \
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
    identifyMe(parser)
    try:
        args.func(args)
    except AttributeError as ae:
        # no parameter - default behaviour: show help
        parser.print_help()
        print("\nError: " + str(ae))
        print(parser)



