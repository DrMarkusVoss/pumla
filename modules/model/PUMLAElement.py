
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

    def printMe(self):
        """ command line print out of the model element attributes """
        print("name: " + self.name)
        print("alias: " + self.alias)
        print("parent: " + self.parent)
        print("path: " + self.path)
        print("filename: " + self.filename)