import os
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


def findElementNameInText(lines, alias):
    """ find the real name of the model element with given alias in given line """
    # return value with '-' as default
    elem_name = "-"
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
    # return the found element name
    return elem_name

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
        el_name = findElementNameInText(lines, el_alias)
        if (el_name == "-"):
            pel.setName(el_alias)
        else:
            pel.setName(el_name)

    # return the PUMLA Element
    return pel
