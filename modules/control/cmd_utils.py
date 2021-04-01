import os
import json
from modules.model.PUMLAElement import PUMLAElement

def findAllPUMLAFiles(path):
    """" find all pumla files in given path """
    pumlafiles = []

    # walk through the file and folder structure
    # and put all PUMLA files into a list
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            # a PUMLA file must end with '.puml' (see Modelling Guideline)
            if fname.endswith('.puml'):
                with open(fname) as myfile:
                    line = myfile.read()
                    # a PUMLA file must have that first comment line (see Modelling Guideline)
                    if (line.startswith("'PUMLAMR")):
                        pumlafiles.append(fname)

    #return the list of PUMLA files found
    return pumlafiles


def findElementNameAndTypeInText(lines, alias):
    """ find the real name of the model element with given alias in given line """
    # return value with '-' as default
    elem_name = "-"
    elem_type = "-"
    # search term definition
    findit = " as " + alias
    for e in lines:
        if (findit in e):
            # a definition of a name that needs an alias is put in '"',
            # therefore there must be two '"' and the name is in between
            if ('"' in e):
                splt = e.rsplit('"')
                # the name must be in the middle, so in list item 2 of 3
                if (len(splt) == 3):
                    # element name is the second item, list starts at 0
                    elem_name = splt[1]
                    elem_type = splt[0].strip()
    # return the found element name
    return elem_name, elem_type

def parsePUMLAFile(filename):
    """ parses a PUMLA file and returns a description of its content as returned PUMLA element."""
    # read contents of file at once
    file = open(filename)
    text = file.read()
    file.close()

    # split the file content per line
    # into a list of lines
    lines = text.split("\n")

    # this element will be filled with information
    # of the file and returned
    pel = PUMLAElement()
    # check if it is a PUMLA file
    if ("'PUMLAMR" in lines[0]):
        # parent is defined by second line comment like below
        if ("'PUMLAPARENT:" in lines[1]):
            par = lines[1].lstrip("'PUMLAPARENT: ")
            parent = par.strip(" ")
            pel.setParent(parent)
        # all other information can be found in filename (Modelling Guideline)
        # and file contents.
        fns = filename.split("/")
        el_fn = fns[len(fns)-1]
        pel.setFilename(el_fn)
        el_alias_s = el_fn.split(".")
        el_alias = el_alias_s[0]
        pel.setAlias(el_alias)
        el_path = filename.rstrip(el_fn)
        pel.setPath(el_path)
        el_name, el_type = findElementNameAndTypeInText(lines, el_alias)
        if (el_name == "-"):
            pel.setName(el_alias)
        else:
            pel.setName(el_name)
        pel.setType(el_type)

    # return the PUMLA Element
    return pel

def serializePUMLAElementsToDict(pumla_elements):
    '''create a dict from the list of pumla elements from which easily a JSON definition can be created'''
    dict = {"elements": []}

    # put the relevant information from each pumla element
    # into a temp dict. put all temp dicts into a
    # dict for all the elements
    for e in pumla_elements:
        tmpdict = {}
        tmpdict["name"] = e.getName()
        tmpdict["alias"] = e.getAlias()
        tmpdict["type"] = e.getType()
        tmpdict["parent"] = e.getParent()
        tmpdict["path"] = e.getPath()
        tmpdict["filename"] = e.getFilename()
        dict["elements"].append(tmpdict)

    return dict

def updatePUMLAMR(path, mrfilename):
    """create, update/overwrite the PUMLA model repository json file with current state of the source code repository"""
    # traverse down the path and find all
    # pumla files.
    pumlafiles = findAllPUMLAFiles(path)

    # parse each pumla file and create
    # a PUMLA Element out of it, that
    # gets put into a list.
    pumlaelements = []
    for f in pumlafiles:
        pel = parsePUMLAFile(f)
        pumlaelements.append(pel)

    # put the elements into a dictionary that can be easily
    # transformed into a JSON representation.
    jsondict = serializePUMLAElementsToDict(pumlaelements)

    # make it accessible from within PlantUML.
    # $allelemens is the preprocessor variable that
    # allows access by PlantUML pumla marcros.
    jsontxt = "!$allelems = " + json.dumps(jsondict)

    # split text to make the resulting file more readable;
    # one element definition per line.
    txt_lines = jsontxt.split("},")

    # write the lines to the model repo file
    with open(mrfilename, "w") as fil:
        for i in range(len(txt_lines)-1):
            fil.write(txt_lines[i] + "},\n")
        fil.write(txt_lines[len(txt_lines)-1] + "\n")
    fil.close()

    return True, mrfilename
