
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
        self.isInstance = False
        self.instance_class_alias = "-"

    def setInstance(self):
        self.isInstance = True

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

    def printMe(self):
        """ command line print out of the model element attributes """
        print("name: " + self.name)
        print("alias: " + self.alias)
        print("type: " + self.type)
        sts = "-"
        if (len(self.stereotypes) > 0):
            sts = "" + self.stereotypes[0]
            for i in range(len(self.stereotypes)-1):
                sts = sts + ", " + self.stereotypes[i+1]

        print("stereotypes: " + sts)
        print("parent: " + self.parent)
        print("path: " + self.path)
        print("filename: " + self.filename)