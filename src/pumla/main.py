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


def cmd_listelements(args):
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


def cmd_update(args):
    """create/update/overwrite the pumla model repository"""
    print("updating...")
    (success, efn) = updatePUMLAMR(os.path.curdir, args.mrefilename)
    if success:
        print("model repo file: " + efn)
        print("done.")
    else:
        print("failed.")


def cmd_listfiles(args):
    print("all pumla files in subdirs:")
    pfls = findAllPUMLAFiles(os.path.curdir)
    for e in pfls:
        print(e)


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
        help="list all `pumla` model elements of the model repository repository",
    )
    parser_listelements.set_defaults(func=cmd_listelements)

    parser_listfiles = subparsers.add_parser(
        "files",
        help="list all `pumla` marked model files of the model repository",
    )
    parser_listfiles.set_defaults(func=cmd_listfiles)

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
    parser_update.set_defaults(func=cmd_update)

    args = parser.parse_args()
    identifyMe(parser)
    try:
        args.func(args)
    except AttributeError:
        # no parameter - default behaviour: show help
        parser.print_help()
