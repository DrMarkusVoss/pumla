
class PUMLARelation:
    ''' store PUMLA relations '''
    def __init__(self, id, start, end, reltype="", reltxt=""):
        self.id = id
        self.start = start
        self.end = end
        self.reltype = reltype
        self.reltxt = reltxt
        self.path = "-"
        self.filename = "-"


    def getID(self):
        return self.id

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getRelType(self):
        return self.reltype

    def getRelTxt(self):
        return self.reltxt

    def getPath(self):
        return self.path

    def getFilename(self):
        return self.filename

    def setPath(self, path):
        self.path = path


    def setFilename(self, fn):
        self.filename = fn

