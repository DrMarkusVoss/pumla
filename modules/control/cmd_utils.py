import os
import json
from modules.model.PUMLAElement import PUMLAElement
from modules.model.PUMLARelation import PUMLARelation
from modules.model.PUMLAConnection import PUMLAConnection

puml_deployment_keywords = ["actor", "agent", "artifact", "boundary", "card", "circle", "cloud",
                            "collections", "component", "control", "database", "entity", "file",
                            "folder", "frame", "hexagon", "interface", "label", "node",
                            "package", "queue", "rectangle", "stack", "storage", "usecase"]


def isPumlDeployKeywordInLine(line):
    """check whether one of the deployment diagram element keywords
        is contained in the given string line."""
    retval = False

    for kw in puml_deployment_keywords:
        if (kw in line):
            retval = True

    return retval

def isInBlacklist(path, blacklist):
    """ check whether the given path is in the blacklist list."""
    retval = False
    for e in blacklist:
        if (e in path):
            retval = True
    return retval

def findAllPUMLAFiles(path):
    """" find all pumla files in given path """
    pumlafiles = []
    blacklist = []

    blacklistfilename = path + "/pumla_blacklist.txt"
    #print(blacklistfilename)
    if (os.path.isfile(blacklistfilename)):
        #print("blacklist found\n")
        file = open(blacklistfilename)
        text = file.read()
        #print(text)
        file.close()
        for li in text.split():
            blacklist.append(path + li.strip("."))
        #print(blacklist)


    # walk through the file and folder structure
    # and put all PUMLA files into a list
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            if (not(isInBlacklist(dirpath, blacklist))):
                #print(dirpath)
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

def findStereoTypesInLine(line):
    """ find PlantUML stereotype definitions in given line. """
    e = line
    stypes = []
    tempstr = e
    for c in range(e.count("<<")):
        st = tempstr[tempstr.find("<<") + 2:tempstr.find(">>")]
        stypes.append(st)
        tempstr = tempstr.replace("<<" + st + ">>", "")

    return stypes

def findElementNameAndTypeInText(lines, alias):
    """ find the real name, type and stereotype(s) of the model element with given alias in given line """
    # return value with '-' as default
    elem_name = "-"
    elem_type = "-"
    elem_stereotypes = []
    # search term definition
    findit = " as " + alias
    # it is tricky to find the element definition as the alias name might also occur in
    # a comment or note.
    for e in lines:
        if (findit in e):
            stypes = findStereoTypesInLine(e)

            for sts in stypes:
                elem_stereotypes.append(sts)


            # a definition of a name that needs an alias is put in '"',
            # therefore there must be two '"' and the name is in between
            if ('"' in e):
                splt = e.rsplit('"')
                # the name must be in the middle, so in list item 2 of 3
                if (len(splt) == 3):
                    # element name is the second item, list starts at 0
                    elem_name = splt[1]
                    elem_type = splt[0].strip()


        elif ((alias in e) and (not("'" in e)) and (isPumlDeployKeywordInLine(e))):
            stypes = findStereoTypesInLine(e)

            for sts in stypes:
                elem_stereotypes.append(sts)
            splt = e.rsplit(alias)
            elem_type = splt[0].strip()
    # return the found element name
    return elem_name, elem_type, elem_stereotypes

def findRelations(lines, path, filename):
    """ find PUMLA relation definitions in given lines. """
    ret_rels = []
    for e in lines:
        if ("PUMLARelation" in e):
            s1 = e.replace("PUMLARelation", "")
            s2 = s1.strip("()")
            s3 = s2.split(",")
            s4 = [ix.strip() for ix in s3]
            s5 = [ix.strip('"') for ix in s4]

            if (len(s4)>4):
                pr = PUMLARelation(s5[4], s5[0], s5[1], s5[2], s5[3])
                pr.setPath(path)
                pr.setFilename(filename)
                ret_rels.append(pr)

    return ret_rels

def findConnections(lines, path, filename):
    """ find PUMLA connection definitions in given lines. """
    ret_cons = []
    for e in lines:
        if ("PUMLAConnection" in e):
            s1 = e.replace("PUMLAConnection", "")
            s2 = s1.strip("()")
            s3 = s2.split(",")
            s4 = [ix.strip() for ix in s3]
            s5 = [ix.strip('"') for ix in s4]

            if (len(s4)>4):
                pr = PUMLAConnection(s5[4], s5[0], s5[1], s5[2], s5[3])
                pr.setPath(path)
                pr.setFilename(filename)
                ret_cons.append(pr)

    return ret_cons

def findInstances(lines, path, filename):
    """ find PUMLA instance definitions in given lines. """
    ret_instances = []
    for e in lines:
        if ("PUMLAInstanceOf(" in e):
            s1 = e.replace("PUMLAInstanceOf", "")
            s2 = s1.strip("()")
            s3 = s2.split(",")
            s4 = [ix.strip() for ix in s3]
            s5 = [ix.strip('"') for ix in s4]

            if (len(s5) > 1):
                pr = PUMLAElement()
                pr.setInstance()
                pr.addStereotype("instance")
                pr.setInstanceClassAlias(s5[0])
                pr.setAlias(s5[1])
                if (len(s5) > 2):
                    pr.setName(s5[2])
                else:
                    pr.setName(s5[1])
                pr.setPath(path)
                pr.setFilename(filename)
                ret_instances.append(pr)

    return ret_instances

def createInstanceRelation(inst, path, fn):
    """ creates a PUMLA instance-of relation for a given instance. """
    pr = PUMLARelation(("REL#" + inst.getAlias() + inst.getInstanceClassAlias()), inst.getAlias(), "..>", inst.getInstanceClassAlias(), "instance of")
    pr.setPath(path)
    pr.setFilename(fn)
    return pr

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
    pels = []
    rels = []
    cons = []
    # check if it is a PUMLA file
    if ("'PUMLAMR" in lines[0]):
        fns = filename.split("/")
        el_fn = fns[len(fns) - 1]
        el_path = filename.rstrip(el_fn)
        # instance definition is defined by second line comment
        if ("'PUMLAINSTANCES" in lines[1]):
            ri = findInstances(lines, el_path, el_fn)
            for i in ri:
                pels.append(i)
                instrel = createInstanceRelation(i, el_path, el_fn)
                rels.append(instrel)

                #i.printMe()
            pass
        # parent is defined by second line comment like below
        else:
            if ("'PUMLAPARENT:" in lines[1]):
                par = lines[1].lstrip("'PUMLAPARENT: ")
                parent = par.strip(" ")
                pel.setParent(parent)
            # all other information can be found in filename (Modelling Guideline)
            # and file contents.
            pel.setFilename(el_fn)
            el_alias_s = el_fn.split(".")
            el_alias = el_alias_s[0]
            pel.setAlias(el_alias)
            pel.setPath(el_path)
            el_name, el_type, el_stereotypes = findElementNameAndTypeInText(lines, el_alias)
            if ((el_name == "-") and (el_type == "-") and (el_stereotypes == [])):
                pel = None
                pels = []
            else:
                if (el_name == "-"):
                    pel.setName(el_alias)
                else:
                    pel.setName(el_name)
                pel.setType(el_type)
                for st in el_stereotypes:
                    pel.stereotypes.append(st)
                pels.append(pel)
            rels = findRelations(lines, el_path, el_fn)
            cons = findConnections(lines, el_path, el_fn)

    # return the PUMLA Element
    return pels, rels, cons

def serializePUMLAElementsToDict(pumla_elements, path, mrfilename):
    '''create a dict from the list of pumla elements from which easily a JSON definition can be created'''
    dict = {"modelrepopath" : os.path.abspath(path), "modelrepofile" : mrfilename, "elements": []}

    # put the relevant information from each pumla element
    # into a temp dict. put all temp dicts into a
    # dict for all the elements
    for e in pumla_elements:
        tmpdict = {}
        tmpdict["name"] = e.getName()
        tmpdict["alias"] = e.getAlias()
        tmpdict["type"] = e.getType()
        tmpdict["stereotypes"] = e.getStereotypes()
        tmpdict["parent"] = e.getParent()
        tmpdict["instclassalias"] = e.getInstanceClassAlias()
        tmpdict["path"] = e.getPath()
        tmpdict["filename"] = e.getFilename()
        dict["elements"].append(tmpdict)

    return dict

def serializePUMLARelationsToDict(rels, mrpath, mrfilename):
    '''create a dict from the list of pumla relations from which easily a JSON definition can be created'''
    dict = {"modelrelationrepopath" : os.path.abspath(mrpath), "modelrelationrepofile" : mrfilename, "relations": []}

    # put the relevant information from each pumla element
    # into a temp dict. put all temp dicts into a
    # dict for all the elements
    for e in rels:
        tmpdict = {}
        tmpdict["id"] = e.getID()
        tmpdict["start"] = e.getStart()
        tmpdict["end"] = e.getEnd()
        tmpdict["reltype"] = e.getRelType()
        tmpdict["reltxt"] = e.getRelTxt()
        tmpdict["path"] = e.getPath()
        tmpdict["filename"] = e.getFilename()
        dict["relations"].append(tmpdict)

    return dict

def serializePUMLAConnectionsToDict(cons, mrpath, mrfilename):
    '''create a dict from the list of pumla relations from which easily a JSON definition can be created'''
    dict = {"modelconnectionrepopath" : os.path.abspath(mrpath), "modelconnectionrepofile" : mrfilename, "connections": []}

    # put the relevant information from each pumla element
    # into a temp dict. put all temp dicts into a
    # dict for all the elements
    for e in cons:
        tmpdict = {}
        tmpdict["id"] = e.getID()
        tmpdict["start"] = e.getStart()
        tmpdict["end"] = e.getEnd()
        tmpdict["contype"] = e.getConType()
        tmpdict["contxt"] = e.getConTxt()
        tmpdict["path"] = e.getPath()
        tmpdict["filename"] = e.getFilename()
        dict["connections"].append(tmpdict)

    return dict

def getElementByAlias(pels, alias):
    retval = None

    for e in pels:
        if (e.getAlias() == alias):
            retval = e
            break

    return retval

def finalizeInstances(pels):
    '''instance information can only be finalized when the repo is fully setup.
    This function adds parent type and stereotypes to the instance.'''
    for e in pels:
        #print(e.getStereotypes())
        if ("instance" in e.getStereotypes()):
            #print("found instance")
            parent = getElementByAlias(pels, e.getInstanceClassAlias())
            for st in parent.getStereotypes():
                e.addStereotype(st)
            e.setType(parent.getType())

    return pels


def updatePUMLAMR(path, mrefilename):
    """create, update/overwrite the PUMLA model repository json file with current state of the source code repository"""
    # traverse down the path and find all
    # pumla files.
    pumlafiles = findAllPUMLAFiles(path)

    # parse each pumla file and create
    # a PUMLA Element out of it, that
    # gets put into a list.
    pumlaelements = []
    pumlarelations = []
    pumlaconnections = []

    # sum up information from all files in common lists
    for f in pumlafiles:
        pels, rels, cons = parsePUMLAFile(f)
        for p in pels:
            pumlaelements.append(p)
        for r in rels:
            pumlarelations.append(r)
        for c in cons:
            pumlaconnections.append(c)

    tmp_pels = finalizeInstances(pumlaelements)

    pumlaelements = tmp_pels

    # put the elements into a dictionary that can be easily
    # transformed into a JSON representation.
    jsondict = serializePUMLAElementsToDict(pumlaelements, path, mrefilename)

    # put the relations into a dictionary that can be easily
    # transformed into a JSON representation.
    jsonreldict = serializePUMLARelationsToDict(pumlarelations, path, mrefilename)

    # put the connections into a dictionary that can be easily
    # transformed into a JSON representation.
    jsoncondict = serializePUMLAConnectionsToDict(pumlaconnections, path, mrefilename)

    # make it accessible from within PlantUML.
    # $allelemens is the preprocessor variable that
    # allows access by PlantUML pumla marcros.
    jsontxt = "!$allelems = " + json.dumps(jsondict)

    # make it accessible from within PlantUML.
    # $allrelations is the preprocessor variable that
    # allows access by PlantUML pumla marcros.
    jsonreltxt = "!$allrelations = " + json.dumps(jsonreldict)

    # make it accessible from within PlantUML.
    # $allconnections is the preprocessor variable that
    # allows access by PlantUML pumla marcros.
    jsoncontxt = "!$allconnections = " + json.dumps(jsoncondict)

    # split text to make the resulting file more readable;
    # one element definition per line.
    txt_lines = jsontxt.split("},")

    # split text to make the resulting file more readable;
    # one element definition per line.
    txtrel_lines = jsonreltxt.split("},")

    # split text to make the resulting file more readable;
    # one element definition per line.
    txtcon_lines = jsoncontxt.split("},")

    # write the lines to the model element repo file
    with open(mrefilename, "w") as fil:
        for i in range(len(txt_lines)-1):
            fil.write(txt_lines[i] + "},\n")
        fil.write(txt_lines[len(txt_lines)-1] + "\n\n")
        for i in range(len(txtrel_lines)-1):
            fil.write(txtrel_lines[i] + "},\n")
        fil.write(txtrel_lines[len(txtrel_lines)-1] + "\n\n")
        for i in range(len(txtcon_lines)-1):
            fil.write(txtcon_lines[i] + "},\n")
        fil.write(txtcon_lines[len(txtcon_lines)-1] + "\n\n")
    fil.close()

    return True, mrefilename
