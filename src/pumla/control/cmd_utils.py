"""The pumla command line tool util functions."""
import os
import json
import shutil
import re
import requests
from os.path import exists
from pumla.model.PUMLAElement import PUMLAElement
from pumla.model.PUMLARelation import PUMLARelation
from pumla.model.PUMLAConnection import PUMLAConnection

puml_deployment_keywords = ["actor", "agent", "artifact", "boundary", "card", "circle", "cloud",
                            "collections", "component", "control", "database", "entity", "file",
                            "folder", "frame", "hexagon", "interface", "label", "node",
                            "package", "queue", "rectangle", "stack", "storage", "usecase"]

puml_class_keywords = ["abstract", "abstract class", "annotation", "circle", "circle_short_form",
                       "class", "diamond", "diamond_short_form", "entity", "enum", "interface"]

puml_dyn_keywords = ["actor", "boundary", "control", "entity", "database",
                       "collections", "participant", "activity", "partition"]

c4_static_keywords = ["Container", "ContainerDb", "ContainerQueue", "Container_Ext", "ContainerDb_Ext",
                      "ContainerQueue_Ext", "Container_Boundary", "Component", "ComponentDb", "ComponentQueue",
                      "Component_Ext", "ComponentDb_Ext", "ComponentQueue_Ext", "Deployment_Node",
                      "Deployment_Node_L", "Deployment_Node_R", "Node", "Node_L", "Node_R",
                      "Person", "Person_Ext", "System", "System_Ext",
                      "System_Boundary", "SystemDb", "SystemQueue", "SystemDb_Ext", "SystemQueue_Ext",
                      "Enterprise_Boundary"]

c4_dynamic_keywords = ["Rel", "Rel_Back", "Rel_Neighbor", "Rel_Back_Neighbor"]

# this is the PlantUML JAR file that will be downloaded to use it for diagram generation
plantuml_jar_download_destiniation = "https://github.com/plantuml/plantuml/releases/download/v1.2023.1/plantuml-1.2023.1.jar"

def gendiagram(mainpath, inputpuml, outputname, picformat):
    pumljar_filename = mainpath + "plantuml-jar/plantuml.jar"
    if not exists(pumljar_filename):
        print("Error: Diagram cannot be generated. PlantUML JAR is not yet installed.")
        print("       Install the PlantUML JAR with the following command before:")
        print("       pumla installplantuml")
    else:
        formatext = "-" + picformat
        os.system("java -jar " + pumljar_filename + " " + inputpuml + " " + formatext)
        print("creating diagram for: " + inputpuml)
        print("done.")

def genpumladiag(mainpath, inputpuml, outputname, layoutoverride):
    pass

def installPlantUMLJAR(mainpath):
    '''downloads the PlantUML JAR file and places it into a pumla command line tool installation directory.'''
    print("downloading...")
    target_filename = mainpath + "plantuml-jar/plantuml.jar"

    succ = False
    if (exists(target_filename)):
        print("Error: the PlantUML JAR file is already installed.")
        print("       If you want it to get updated, please delete the existing JAR file ")
        print("       from the following location manually and call the installation command")
        print("       again.")
        print(target_filename)
        succ = False
    else:
        r = requests.get(plantuml_jar_download_destiniation)
        with open(target_filename, 'wb') as f:
            f.write(r.content)
        succ = exists(target_filename)
    return succ


def checkElsRelsConsForAliasExistence(elements, relations, connections, aliasnametocheck):
    '''search the given lists of elements, relations and connections for the existence of an alias or id with
    the given aliasnametocheck'''
    alias_already_existing = False
    print("now checking for alias: ", aliasnametocheck)
    for el in elements["elements"]:
        if el["alias"] == aliasnametocheck:
            alias_already_existing = True
            print("alias already exists for this element:")
            print(el)
    for rel in relations["relations"]:
        if rel["id"] == aliasnametocheck:
            alias_already_existing = True
            print("alias already exists as id for this relation:")
            print(rel)
    for con in connections["connections"]:
        if con["id"] == aliasnametocheck:
            alias_already_existing = True
            print("alias already exists as id for this connection:")
            print(con)

    return alias_already_existing

def readPumlaMacrosPathFromFile(mainpath):
    '''read the path of the pumla macros location from the file "pumla_macros_path.txt".'''
    pmpath = ""
    success = True
    pmpf = mainpath + "pumla_macros_path.txt"
    if os.path.isfile(pmpf):
        file = open(pmpf)
        firstline = file.readline()
        file.close()
        pmpath = firstline.strip()
    else:
        print("pumla error: pumla not yet properly installed. File 'pumla_macros_path.txt' not found.")
        print("             Please call 'pumla setup' in the pumla source directory.")
        success = False

    return success, pmpath

def createPumlaMacrosFile(mainpath):
    '''create a trampoline include file to include the pumla macros for
       a project at whatever location.'''
    success = True
    pmpsuccess, pumla_macros_path = readPumlaMacrosPathFromFile(mainpath)
    if pmpsuccess:
        curpath = os.path.abspath(os.path.curdir)
        print("Path to initialise: " + curpath + "/")
        print("Path of pumla installation: " + mainpath)
        print("Path of pumla macros: " + pumla_macros_path)

        # filename for the pumla macros in the
        # source code repo where it gets
        # initialised
        pumla_macros_fn = "pumla_macros.puml"
        pm_comment = "' THIS IS AN AUTOMATICALLY GENERATED FILE BY pumla init \n"
        pm_comment = pm_comment + "' DO NOT CHANGE MANUALLY!\n"
        pm_comment = pm_comment + "' TO ADOPT THE PATHS TO YOUR SYSTEM, CALL pumla init AGAIN\n"
        pm_comment = pm_comment + "' IN THE FOLDER OF THIS FILE HERE!\n"
        pm_include_macros = "!include " + pumla_macros_path + "pumla_macros_global.puml\n"
        pm_include_tv = "!include " + pumla_macros_path + "pumla_tagged_values.puml\n"
        pm_include_reqs = "!include " + pumla_macros_path + "pumla_macros_reqs.puml\n"
        pm_include_project_cfg = '\n!if %file_exists("' + curpath + '/pumla_project_config.puml")\n'
        pm_include_project_cfg = pm_include_project_cfg +  "!include pumla_project_config.puml\n"
        pm_include_project_cfg = pm_include_project_cfg + "!endif\n"
        # the C4 integration needs to be included after the project-specific config, as that
        # sets the global variable that defines whether the C4 model integration shall be
        # included or not
        pm_include_c4int = "\n!if ($PUMUseC4Model == %true())\n"
        pm_include_c4int = pm_include_c4int + "!include "+ pumla_macros_path +"pumla_macros_c4int.puml\n"
        pm_include_c4int = pm_include_c4int + "!endif\n"

        with open(pumla_macros_fn, "w") as fil:
            fil.write(pm_comment)
            fil.write(pm_include_project_cfg)
            fil.write(pm_include_macros)
            fil.write(pm_include_tv)
            fil.write(pm_include_reqs)
            fil.write(pm_include_c4int)
        fil.close()
    else:
        success = False

    return success


def createPumlaBlacklistFile():
    '''create an empty pumla_blacklist.txt file'''
    curpath = os.path.abspath(os.path.curdir)
    print("Creating pumla_blacklist.txt here: " + curpath + "/")

    # filename for the pumla macros in the
    # source code repo where it gets
    # initialised
    pumla_blacklist_fn = "pumla_blacklist.txt"
    pm_comment = "# add here folders and files to be ignored\n# for a pumla update scan\n\n"
    with open(pumla_blacklist_fn, "w") as fil:
        fil.write(pm_comment)
    fil.close()

def createPumlaProjectConfigFile(mainpath):
    '''create a project-specific default file for pumla global variables.'''
    success = True
    pmpsuccess, pmp = readPumlaMacrosPathFromFile(mainpath)
    if pmpsuccess:
        curpath = os.path.abspath(os.path.curdir) + "/"
        print("Creating pumla_global_cfg.puml file here: " + curpath)
        srcfile = pmp + "pumla_global_cfg.puml"
        destfile = curpath + "pumla_project_config.puml"
        shutil.copy(srcfile, destfile)
    else:
        success = False

    return success


def pumlaSetup(mainpath):
    '''create the pumla_macros_path.txt file at the location of the pumla installation
       referring to the current directory.'''
    curpath = os.path.abspath(os.path.curdir) + "/"
    print("Creating pumla_macros_path.txt here: " + mainpath)

    # filename for the pumla macros in the
    # source code repo where it gets
    # initialised
    pumla_blacklist_fn = mainpath + "pumla_macros_path.txt"
    pm_comment = curpath + "\n"
    with open(pumla_blacklist_fn, "w") as fil:
        fil.write(pm_comment)
    fil.close()

def pumlaVersionCheck(mainpath, pumla_pycli_version):
    '''check whether the version of the pumla python CLI tool and the
       pumla_macros_global.puml are the same.'''
    success = True
    pmpsucc, pmpath = readPumlaMacrosPathFromFile(mainpath)

    pmg = pmpath + "pumla_macros_global.puml"

    if os.path.isfile(pmg):
        file = open(pmg)
        firstline = file.readline()
        file.close()
        rm1 = firstline.replace("!$PUMLAVersionNumber =", "")
        rm2 = rm1.replace("v", "")
        rm3 = rm2.replace('"', '')
        pumla_macro_version = rm3.strip()
        print("pumla macros version: " + pumla_macro_version)
        print("pumla python CLI tool version: " + pumla_pycli_version)

        if not pumla_macro_version ==  pumla_pycli_version:
            print("pumla error: installation broken. Different versions of CLI tool and macros.")
            print("             PLEASE MAKE A CLEAN NEW INSTALL!")
            success = False
    else:
        print("pumla error: installation broken. No 'pumla_macros_global.puml' file found.")
        print("             PLEASE MAKE A CLEAN NEW INSTALL!")
        success = False

    return success

def isPumlKeywordInLine(line):
    """check whether one of the deployment diagram element keywords
        is contained in the given string line."""
    retval = False

    for kw in puml_deployment_keywords:
        if kw in line:
            retval = True

    for kw in puml_class_keywords:
        if kw in line:
            retval = True

    for kw in puml_dyn_keywords:
        if kw in line:
            retval = True


    return retval

def isInBlacklist(path, blacklist):
    """ check whether the given path is contained in the
        given blacklist list."""
    retval = False
    for e in blacklist:
        if e in path:
            retval = True
    return retval

def readBlacklist(path, pathfilename):
    blacklist = []
    if os.path.isfile(pathfilename):
        # print("readBlackList: blacklist found\n")
        file = open(pathfilename)
        text = file.read()
        file.close()
        for li in text.splitlines():
            # comments in blacklist start with the hash,
            # they are ignored
            if not li.startswith("#") and not li == "":
                blacklist.append(path + li.strip("."))

    return blacklist

def findAllPUMLAFiles(path):
    """" find all pumla files in given path """
    pumlafiles = []
    pumladiagramfiles = []
    blacklist = []

    blacklistfilename = path + "/pumla_blacklist.txt"

    blacklist = readBlacklist(path, blacklistfilename)

    # walk through the file and folder structure
    # and put all PUMLA files into a list
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            if not isInBlacklist(dirpath, blacklist):
                #print(dirpath)
                fname = os.path.join(dirpath, filename)
                # a PUMLA file must end with '.puml' (see Modelling Guideline)
                if fname.endswith('.puml'):
                    with open(fname) as myfile:
                        line = myfile.read()
                        # a PUMLA file must have that first comment line (see Modelling Guideline)
                        if line.startswith("'PUMLAMR"):
                            pumlafiles.append(fname)
                        elif line.startswith("'PUMLADR"):
                            pumladiagramfiles.append(fname)

    #return the list of PUMLA files found
    return pumlafiles, pumladiagramfiles

def findTaggedValuesInText(lines):
    rettvs = []

    ret_cons = []
    for e in lines:
        if "PUMLAAddTaggedValue" in e:
            s1 = e.replace("PUMLAAddTaggedValue", "")
            s2 = s1.strip("()")
            s3 = s2.split(",")
            s4 = [ix.strip() for ix in s3]
            s5 = [ix.strip('"') for ix in s4]

            if len(s4) > 2:
                al_tv = {s5[0] : {s5[1] : s5[2]}}
                rettvs.append(al_tv)

    return rettvs

def findRUATaggedValuesInText(lines, rua_alias):
    rettvs = []

    ret_cons = []
    for e in lines:
        if "PUMLARUAAddTaggedValue" in e:
            s1 = e.replace("PUMLARUAAddTaggedValue", "")
            s2 = s1.strip("()")
            s3 = s2.split(",")
            s4 = [ix.strip() for ix in s3]
            s5 = [ix.strip('"') for ix in s4]

            if len(s4) > 1:
                al_tv = {rua_alias : {s5[0] : s5[1]}}
                rettvs.append(al_tv)

    return rettvs


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
    """ find the real name, type and stereotype(s) of the model
        element with given alias in given line """
    # return value with '-' as default
    elem_name = "-"
    elem_type = "-"
    elem_stereotypes = []
    # search term definition
    findit = " as " + str(alias)
    # it is tricky to find the element definition as the alias name might also occur in
    # a comment or note.
    for e in lines:
        if findit in e:
            stypes = findStereoTypesInLine(e)

            for sts in stypes:
                elem_stereotypes.append(sts)

            # a definition of a name that needs an alias is put in '"',
            # therefore there must be two '"' and the name is in between
            if '"' in e:
                splt = e.rsplit('"')
                # the name must be in the middle, so in list item 2 of 3
                if len(splt) == 3:
                    # element name is the second item, list starts at 0
                    elem_name = splt[1]
                    elem_type = splt[0].strip()


        elif (str(alias) in e) and (not("'" in e)) and (not('"' in e)) and (isPumlKeywordInLine(e)):
            stypes = findStereoTypesInLine(e)
            elem_name = alias

            for sts in stypes:
                elem_stereotypes.append(sts)
            splt = e.rsplit(alias)
            elem_type = splt[0].strip()

    # return the found element name
    return elem_name, elem_type, elem_stereotypes


def findRelations(lines, path, filename):
    """ find PUMLA relation definitions in given lines. """
    pattern_pumlarel = r'PUMLARelation\(\s*\"?(\w+)\"?\s*,\s*\"[-<>\.]+\"\s*,\s*\"?(\w+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*\)'
    pattern_pumlac4rel_gen = r'PUMLAC4Rel(_[UDLR])?\(\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*(,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*)?\)'
    pattern_pumlac4rel_spec = r'PUMLAC4Rel(_\w+)\(\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*(,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*)?\)'
    pattern_pumlac4birel_neigh = r'PUMLAC4BiRel_Neighbor\(\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*(,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*)?\)'
    pattern_pumlac4birel_gen = r'PUMLAC4BiRel(_[UDLR])?\(\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*(,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*)?\)'

    ret_rels = []
    for e in lines:
        # Todo: use Regex for PUMLARelation
        if "PUMLARelation" in e:
            s1 = e.replace("PUMLARelation", "")
            s2 = s1.strip("()")
            s3 = s2.split(",")
            s4 = [ix.strip() for ix in s3]
            s5 = [ix.strip('"') for ix in s4]

            if len(s4) > 4:
                pr = PUMLARelation(s5[4], s5[0], s5[1], s5[2], s5[3])
                pr.setPath(path)
                pr.setFilename(filename)
                ret_rels.append(pr)

        result_c4rel_gen = re.findall(pattern_pumlac4rel_gen, e)
        if result_c4rel_gen:
            #(self, id, start, reltype, end, reltxt="", techntxt="")
            label = ""
            techn = ""
            label = result_c4rel_gen[0][4]
            techn = result_c4rel_gen[0][6]
            pr = PUMLARelation(result_c4rel_gen[0][1], result_c4rel_gen[0][2], "C4Rel" + result_c4rel_gen[0][0], result_c4rel_gen[0][3], label, techn)
            pr.setPath(path)
            pr.setFilename(filename)
            ret_rels.append(pr)

        result_c4rel_spec = re.findall(pattern_pumlac4rel_spec, e)
        if result_c4rel_spec:
            if ("Rel" + result_c4rel_spec[0][0]) in c4_dynamic_keywords:
                #(self, id, start, reltype, end, reltxt="", techntxt="")
                label = ""
                techn = ""
                label = result_c4rel_spec[0][4]
                techn = result_c4rel_spec[0][6]
                pr = PUMLARelation(result_c4rel_spec[0][1], result_c4rel_spec[0][2], "C4Rel" + result_c4rel_spec[0][0], result_c4rel_spec[0][3], label, techn)
                pr.setPath(path)
                pr.setFilename(filename)
                ret_rels.append(pr)

        result_c4birel_gen = re.findall(pattern_pumlac4birel_gen, e)
        if result_c4birel_gen:
            # (self, id, start, reltype, end, reltxt="", techntxt="")
            label = ""
            techn = ""
            label = result_c4birel_gen[0][4]
            techn = result_c4birel_gen[0][6]
            pr = PUMLARelation(result_c4birel_gen[0][1], result_c4birel_gen[0][2], "C4BiRel" + result_c4birel_gen[0][0],
                               result_c4birel_gen[0][3], label, techn)
            pr.setPath(path)
            pr.setFilename(filename)
            ret_rels.append(pr)

        result_c4birel_neigh = re.findall(pattern_pumlac4birel_neigh, e)
        if result_c4birel_neigh:
            # (self, id, start, reltype, end, reltxt="", techntxt="")
            label = ""
            techn = ""
            label = result_c4birel_neigh[0][3]
            techn = result_c4birel_neigh[0][5]
            pr = PUMLARelation(result_c4birel_neigh[0][0], result_c4birel_neigh[0][1], "C4BiRel_Neigh",
                               result_c4birel_neigh[0][2], label, techn)
            pr.setPath(path)
            pr.setFilename(filename)
            ret_rels.append(pr)

    return ret_rels


def findConnections(lines, path, filename):
    """ find PUMLA connection definitions in given lines. """
    ret_cons = []
    for e in lines:
        if "PUMLAConnection" in e:
            s1 = e.replace("PUMLAConnection", "")
            s2 = s1.strip("()")
            s3 = s2.split(",")
            s4 = [ix.strip() for ix in s3]
            s5 = [ix.strip('"') for ix in s4]

            if len(s4)>4:
                pr = PUMLAConnection(s5[4], s5[0], s5[1], s5[2], s5[3])
                pr.setPath(path)
                pr.setFilename(filename)
                ret_cons.append(pr)

    return ret_cons

def findInstances(lines, path, filename, kind):
    """ find PUMLA instance definitions in given lines. """
    ret_instances = []
    for e in lines:
        if "PUMLAInstanceOf(" in e:
            s1 = e.replace("PUMLAInstanceOf", "")
            s2 = s1.strip("()")
            s3 = s2.split(",")
            s4 = [ix.strip() for ix in s3]
            s5 = [ix.strip('"') for ix in s4]

            if len(s5) > 1:
                pr = PUMLAElement()
                pr.setInstance()
                pr.addStereotype("instance")
                pr.setInstanceClassAlias(s5[0])
                pr.setAlias(s5[1])

                if kind == "static":
                    pr.setKindStatic()
                elif kind == "dynamic":
                    pr.setKindDynamic()
                else:
                    print("FindInstances:Error: no meaningful element kind.")
                    pass

                if len(s5) > 2:
                    pr.setName(s5[2])
                else:
                    pr.setName(s5[1])
                pr.setPath(path)
                pr.setFilename(filename)
                ret_instances.append(pr)

        if "PUMLAFullInstanceOf(" in e:
            s1 = e.replace("PUMLAFullInstanceOf", "")
            s2 = s1.strip("()")
            s3 = s2.split(",")
            s4 = [ix.strip() for ix in s3]
            s5 = [ix.strip('"') for ix in s4]

            if len(s5) > 1:
                pr = PUMLAElement()
                pr.setInstance()
                pr.addStereotype("instance")
                pr.setInstanceClassAlias(s5[0])
                pr.setAlias(s5[1])

                if kind == "static":
                    pr.setKindStatic()
                elif kind == "dynamic":
                    pr.setKindDynamic()
                else:
                    print("FindInstances:Error: no meaningful element kind.")
                    pass

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

def parsePUMLAFileMarkings(lines):
    retdict_filemarkings = {"mr": False, "parent": "-", "instances": False, "kind": "-"}

    for e in lines:
        if ("'PUMLAMR" in e):
            retdict_filemarkings["mr"] = True
        elif ("'PUMLAINSTANCES" in e):
            retdict_filemarkings["instances"] = True
        elif ("'PUMLAPARENT:" in e):
            par = e.lstrip("'PUMLAPARENT: ")
            parent = par.strip(" ")
            retdict_filemarkings["parent"] = parent
        elif ("'PUMLADYN" in e):
            retdict_filemarkings["kind"] = "dynamic"
        else:
            pass

    if ((retdict_filemarkings["mr"] == True) and (retdict_filemarkings["kind"] == "-")):
        retdict_filemarkings["kind"] = "static"

    return retdict_filemarkings


def findReUsableAssetDefinition(lines):
    """find pumla RUA definitions in the given lines. According to rules, there is only
       one RUA element allowed per file. With this algo, the last found definition wins.
       But it is an error anyways, if there is more."""

    # TBD: error messages when more than one RUA definition is found in a file.

    # the regex patterns
    pattern_rua = r'PUMLAReUsableAsset\(\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?(\w+)\"?\s*(,\s*\"(\s*(<<[\w\s]+>>\s*)+)\"\s*)?\)'
    pattern_ruaclass = r'PUMLAReUsableClass\(\s*\"?(\w+)\"?\s*(,\s*\"(\s*(<<[\w\s]+>>\s*)+)\"\s*)?\)'
    pattern_ruainst = r'PUMLAFullyInstantiableClass\(\s*\"?(\w+)\"?\s*(,\s*\"(\s*(<<[\w\s]+>>\s*)+)\"\s*)?\)'
    pattern_sts = r'<<[\w\s]+>>'

    pattern_ruaport = r'PUMLARUAPort\(\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*,\s*\"?(\w*)\"?\s*,\s*\"?(\w+)\"?\s*\)'
    pattern_ruaportin = r'PUMLARUAPortIn\(\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*,\s*\"?(\w*)\"?\s*,\s*\"?(\w+)\"?\s*\)'
    pattern_ruaportout = r'PUMLARUAPortOut\(\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*,\s*\"?(\w*)\"?\s*,\s*\"?(\w+)\"?\s*\)'

    pattern_ruatypedif = r'PUMLARUATypedInterface\(\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*,\s*\"?(\w*)\"?\s*,\s*\"?(\w+)\"?\s*,\s*\"?(\w*)\"?\s*\)'

    # todo: parse PUMLA Interfaces and TypedInterfaces

    # generic regex pattern for static C4 elements
    pattern_c4static_gen = r'PUMLAC4(\w+)\(\s*\"?(\w+)\"?\s*,\s*\"?([\w\s\(\),.;:#/\*\+\[\]\{\}]+)\"?\s*(.*)\)'

    success = False
    el_name = ""
    el_alias = ""
    el_type = ""
    # list of stereotypes (without "<<>>")
    el_stereotypes = []
    # list of list:
    # each element: [<portname>, <porttype>, <portalias>]
    el_ports = []
    el_typedifs = []

    for e in lines:
        result_rua = re.findall(pattern_rua, e)
        # I do not expect more than one finding per line... if so, only the first will be considered.
        if result_rua:
            el_name = result_rua[0][0]
            el_alias = result_rua[0][1]
            el_type = result_rua[0][2]

            if not result_rua[0][4] == "":
                stslist = re.findall(pattern_sts, result_rua[0][4])

                for est in stslist:
                    if (est != ""):
                        el_stereotypes.append(est.strip("<>"))
            success = True

        result_port = re.findall(pattern_ruaport, e)
        # I do not expect more than one finding per line... if so, only the first will be considered.
        if result_port:
            port_name = result_port[0][0]
            port_alias = result_port[0][2]
            port_type = result_port[0][1]

            if port_type == "":
                port_type = "-"


            el_ports.append({"name": port_name, "interfacetype": port_type, "type": "inout", "alias": port_alias, "taggedvalues": []})

            success = True

        result_portin = re.findall(pattern_ruaportin, e)
        # I do not expect more than one finding per line... if so, only the first will be considered.
        if result_portin:
            portin_name = result_portin[0][0]
            portin_alias = result_portin[0][2]
            portin_type = result_portin[0][1]

            if portin_type == "":
                portin_type = "-"

            el_ports.append({"name": portin_name, "interfacetype": portin_type, "type": "in", "alias": portin_alias, "taggedvalues": []})

            success = True

        result_portout = re.findall(pattern_ruaportout, e)
        # I do not expect more than one finding per line... if so, only the first will be considered.
        if result_portout:
            portout_name = result_portout[0][0]
            portout_alias = result_portout[0][2]
            portout_type = result_portout[0][1]

            if portout_type == "":
                portout_type = "-"

            el_ports.append({"name": portout_name, "interfacetype": portout_type, "type": "out", "alias": portout_alias, "taggedvalues": []})

            success = True

        result_ruatypedif = re.findall(pattern_ruatypedif, e)
        # I do not expect more than one finding per line... if so, only the first will be considered.
        if result_ruatypedif:
            if_name = result_ruatypedif[0][0]
            if_alias = result_ruatypedif[0][2]
            if_type = result_ruatypedif[0][1]
            typedif_type = result_ruatypedif[0][3]

            if if_type == "":
                if_type = "-"

            if typedif_type == "":
                typedif_type = "inout"

            el_typedifs.append({"name": if_name, "interfacetype": if_type, "type": typedif_type, "alias": if_alias,
                             "taggedvalues": []})

            success = True

        result_ruaclass = re.findall(pattern_ruaclass, e)
        if result_ruaclass:
            el_alias = result_ruaclass[0][0]
            el_name = el_alias
            el_type = "class"

            if not result_ruaclass[0][2] == "":
                stslist = re.findall(pattern_sts, result_ruaclass[0][2])

                for est in stslist:
                    if (est != ""):
                        el_stereotypes.append(est.strip("<>"))
            success = True

        result_ruainstclass = re.findall(pattern_ruainst, e)
        if result_ruainstclass:
            el_alias = result_ruainstclass[0][0]
            el_name = el_alias
            el_type = "class"

            if not result_ruainstclass[0][2] == "":
                stslist = re.findall(pattern_sts, result_ruainstclass[0][2])

                for est in stslist:
                    if (est != ""):
                        el_stereotypes.append(est.strip("<>"))
            success = True

        result_c4static_gen = re.findall(pattern_c4static_gen, e)
        if result_c4static_gen:
            if result_c4static_gen[0][0] in c4_static_keywords:
                el_alias = result_c4static_gen[0][1]
                el_name = result_c4static_gen[0][2]
                el_type = "C4" + result_c4static_gen[0][0]
                success = True

    return success, el_name, el_alias, el_type, el_stereotypes, el_ports, el_typedifs


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
    tvs = {}
    # check if it is a PUMLA file
    file_markings = parsePUMLAFileMarkings(lines)
    #print(filename)
    #print(file_markings)
    if (file_markings["kind"] == "static"):
        pel.setKindStatic()
    elif (file_markings["kind"] == "dynamic"):
        pel.setKindDynamic()
    else:
        print("ParsePumlaFile:Error: no meaningful element kind.")
        pass

    if ("'PUMLAMR" in lines[0]):
        fns = filename.split("/")
        el_fn = fns[len(fns) - 1]
        el_path = filename.rstrip(el_fn)
        # instance definition is defined by second line comment
        if ("'PUMLAINSTANCES" in lines[1]):
            ri = findInstances(lines, el_path, el_fn, file_markings["kind"])
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
            # only if not found, check for old syntax...
            success, el_name, el_alias, el_type, el_stereotypes, el_ports, el_typedifs = findReUsableAssetDefinition(lines)
            pel.setPath(el_path)
            if not(success):
                el_alias_s = el_fn.split(".")
                el_alias = el_alias_s[0]
                el_name, el_type, el_stereotypes = findElementNameAndTypeInText(lines, el_alias)

            pel.setAlias(el_alias)
            tvs = findTaggedValuesInText(lines)
            tvs2 = findRUATaggedValuesInText(lines, el_alias)
            for tava in tvs2:
                tvs.append(tava)

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

                for p in el_ports:
                    pel.addPort(p)

                for ti in el_typedifs:
                    pel.addTypedIf(ti)

                pels.append(pel)
            rels = findRelations(lines, el_path, el_fn)
            cons = findConnections(lines, el_path, el_fn)

    # return the PUMLA Element
    return pels, rels, cons, tvs

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
        tmpdict["ports"] = e.getPorts()
        tmpdict["typed_ifs"] = e.getTypedIfs()
        tmpdict["kind"] = e.getKind()
        tmpdict["parent"] = e.getParent()
        tmpdict["instclassalias"] = e.getInstanceClassAlias()
        tmpdict["path"] = e.getPath()
        tmpdict["filename"] = e.getFilename()
        tvs = e.getTaggedValuesMRJSONFormat()
        # the tagged values are stored in a dict
        if (tvs.__len__() > 0):
            tmpdict["taggedvalues"] = tvs
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
        tmpdict["techntxt"] = e.getTechnTxt()
        tmpdict["path"] = e.getPath()
        tmpdict["filename"] = e.getFilename()
        tvs = e.getTaggedValuesMRJSONFormat()
        # the tagged values are stored in a dict
        if (tvs.__len__() > 0):
            tmpdict["taggedvalues"] = tvs
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
        tvs = e.getTaggedValuesMRJSONFormat()
        # the tagged values are stored in a dict
        if (tvs.__len__() > 0):
            tmpdict["taggedvalues"] = tvs
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
            if (parent == None):
                print("PUMLA model error: parent not found for instance with alias: " + e.getAlias() + "; missing parent element is: " + e.getInstanceClassAlias())
            else:
                for st in parent.getStereotypes():
                    e.addStereotype(st)
                e.setType(parent.getType())

    return pels

def getIndexForElementInList(el_alias, pels):
    retval = -1
    index = 0

    for e in pels:
        if (e.getAlias() == el_alias):
            retval = index
            break
        index = index + 1

    return retval

def getIndexForPortInList(el_alias, pels):
    retval_ind = -1
    retval_pind  = -1
    index = 0
    pindex = 0

    for e in pels:
        for p in e.getPorts():
            if (p["alias"] == el_alias):
                retval_ind = index
                retval_pind = pindex
            break
            pindex = pindex + 1
        pindex = 0
        index = index + 1

    return retval_ind, retval_pind

def getIndexForConnectionInList(con_id, cons):
    retval = -1
    index = 0

    for e in cons:
        if (e.getID() == con_id):
            retval = index
            break
        index = index + 1

    return retval

def addTaggedValueToPort(port, tag, value):
    """add a tagged value to a port of a reusable element."""
    found = False
    for tvp in port["taggedvalues"]:
        if tvp["tag"] == tag:
            found = True
            tvp["values"].append(value)
    if not(found):
        port["taggedvalues"].append({"tag": tag, "values": [value]})


def addTaggedValuesToElements(tvs, pels):

    if (tvs.__len__() > 0):
        for t in tvs:
            #print(t)
            for k in t.keys():
                ind = getIndexForElementInList(k, pels)
                pe_ind, pe_pind = getIndexForPortInList(k, pels)
                if (ind != -1):
                    for tv in t[k]:
                        pels[ind].addTaggedValue(tv, t[k][tv])
                if (pe_ind != -1):
                    for tv in t[k]:
                        ports = pels[pe_ind].getPorts()
                        addTaggedValueToPort(ports[pe_pind], tv, t[k][tv])


    return pels

def addTaggedValuesToCons(tvs, cons):

    if (tvs.__len__() > 0):
        for t in tvs:
            #print(t)
            for k in t.keys():
                ind = getIndexForConnectionInList(k, cons)
                if (ind == -1):
                    break
                #print("ind =" + str(ind))
                #print("el_al = " + cons[ind].getID())
                #cons[ind].printMe()
                for tv in t[k]:
                    #print("tv")
                    #print(tv)
                    #print(t[k][tv])
                    cons[ind].addTaggedValue(tv, t[k][tv])

    return cons

def addTaggedValuesToRels(tvs, rels):

    if (tvs.__len__() > 0):
        for t in tvs:
            #print(t)
            for k in t.keys():
                ind = getIndexForConnectionInList(k, rels)
                if (ind == -1):
                    break
                #print("ind =" + str(ind))
                #print("el_al = " + cons[ind].getID())
                #cons[ind].printMe()
                for tv in t[k]:
                    #print("tv")
                    #print(tv)
                    #print(t[k][tv])
                    rels[ind].addTaggedValue(tv, t[k][tv])

    return rels

def updatePUMLAMR(path, mrefilename):
    """create, update/overwrite the PUMLA model repository json file
        with current state of the source code repository"""
    # traverse down the path and find all
    # pumla files.
    pumlafiles, pumladiagfiles = findAllPUMLAFiles(path)

    # parse each pumla file and create
    # a PUMLA Elements, Connections and
    # relations out of it, that
    # get put into lists.
    pumlaelements = []
    pumlarelations = []
    pumlaconnections = []
    pumlataggedvalues = []

    # sum up information from all files in common lists
    for f in pumlafiles:
        pels, rels, cons, tvs = parsePUMLAFile(f)
        for p in pels:
            pumlaelements.append(p)
        for r in rels:
            pumlarelations.append(r)
        for c in cons:
            pumlaconnections.append(c)

        npumlels = addTaggedValuesToElements(tvs, pumlaelements)
        npumlcons = addTaggedValuesToCons(tvs, pumlaconnections)
        npumlrels = addTaggedValuesToRels(tvs, pumlarelations)

    # finalization step necessary to complement the instances
    # with information from the parents. that can only be done
    # when the complete repo has been created, so that all
    # parents for the instances are within the repo list.
    # then the instances can be complemented with information
    # from their parents: type and stereotypes.
    tmp_pels = finalizeInstances(pumlaelements)

    pumlaelements = tmp_pels

    # put the elements into a dictionary that can be easily
    # transformed into a JSON representation.
    jsonelemdict = serializePUMLAElementsToDict(pumlaelements, path, mrefilename)

    # put the relations into a dictionary that can be easily
    # transformed into a JSON representation.
    jsonreldict = serializePUMLARelationsToDict(pumlarelations, path, mrefilename)

    # put the connections into a dictionary that can be easily
    # transformed into a JSON representation.
    jsoncondict = serializePUMLAConnectionsToDict(pumlaconnections, path, mrefilename)

    # make it accessible from within PlantUML.
    # $allelemens is the preprocessor variable that
    # allows access by PlantUML pumla marcros.
    jsontxt = "!$allelems = " + json.dumps(jsonelemdict)

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

    return True, mrefilename, jsonelemdict, jsonreldict, jsoncondict
