"""Class describing a model element."""
class PUMLAElement:
    """ class describing an atomic PUMLA model element """

    def __init__(self):
        """ init every attribute with '-' as default, nothing more """
        self.name = "-"
        self.alias = "-"
        self.type = "-"
        self.parent = "-"
        self.filename = "-"
        self.path = "-"
        self.stereotypes = []
        # list of list:
        # each element: [<portname>, <porttype>, <portalias>]
        self.ports = []
        self.typed_ifs = []
        self.is_instance = False
        self.instance_class_alias = "-"
        # can be "static" or "dynamic"
        self.kind = "-"
        # tagged values is a dict are like
        # like {<tag>: [<tag_value1>, <tag_value2>, ...]}
        self.tagged_values = {}

    def setKindStatic(self):
        self.kind = "static"

    def setKindDynamic(self):
        self.kind = "dynamic"

    def getKind(self):
        return self.kind

    def setInstance(self):
        self.is_instance = True

    def setInstanceClassAlias(self, ic):
        self.instance_class_alias = ic

    def getInstanceClassAlias(self):
        return self.instance_class_alias

    def setName(self, name):
        """ setter for 'name' """
        self.name = name

    def setType(self, type):
        self.type = type

    def setFilename(self, filename):
        """ setter for 'filename' """
        self.filename = filename

    def setParent(self, parent):
        """ setter for 'parent' """
        self.parent = parent

    def setAlias(self, alias):
        """ setter for 'alias' """
        self.alias = alias

    def setPath(self, path):
        """ setter for 'path' """
        self.path = path

    def addStereotype(self, st):
        self.stereotypes.append(st)

    def addPort(self, port):
        self.ports.append(port)

    def addTypedIf(self, typedif):
        self.typed_ifs.append(typedif)

    def setPorts(self, ports):
        self.ports = ports

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getAlias(self):
        return self.alias

    def getParent(self):
        return self.parent

    def getPath(self):
        return self.path

    def getFilename(self):
        return self.filename

    def getStereotypes(self):
        return self.stereotypes

    def getPorts(self):
        return self.ports

    def getTypedIfs(self):
        return self.typed_ifs

    def getTaggedValues(self):
        return self.tagged_values

    def getTaggedValuesMRJSONFormat(self):
        tvs = []
        for k in self.tagged_values.keys():
            nd = {"tag" : k, "values" : self.tagged_values[k]}
            tvs.append(nd)

        return tvs

    def addTaggedValue(self, tag, value):
        """add a tagged value."""
        if tag in self.tagged_values:
            self.tagged_values[tag].append(value)
        else:
            self.tagged_values[tag] = [value]

    def addValueToTag(self, value, tag):
        """add a value to a already existing tag."""
        self.tagged_values[tag].append(value)

    def printMe(self):
        """ command line print out of the model element attributes """
        print("name: " + self.name)
        print("alias: " + self.alias)
        print("type: " + self.type)
        sts = "-"
        if len(self.stereotypes) > 0:
            sts = "" + self.stereotypes[0]
            for i in range(len(self.stereotypes)-1):
                sts = sts + ", " + self.stereotypes[i+1]

        print("stereotypes: " + sts)
        print("ports:")
        for p in self.ports:
            print("\t" + p["name"] + " (" + p["interfacetype"] + ") : " + p["type"])
        print("typed interfaces:")
        for ti in self.typed_ifs:
            print("\t" + ti["name"] + " (" + ti["interfacetype"] + ") : " + p["type"])
        print("parent: " + self.parent)
        print("path: " + self.path)
        print("filename: " + self.filename)


