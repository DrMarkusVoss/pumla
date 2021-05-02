
class PUMLAConnection:
    ''' store PUMLA connections '''
    def __init__(self, id, start, contype, end, contxt=""):
        self.id = id
        self.start = start
        self.end = end
        self.contype = contype
        self.contxt = contxt
        self.path = "-"
        self.filename = "-"


    def getID(self):
        return self.id

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getConType(self):
        return self.contype

    def getConTxt(self):
        return self.contxt

    def getPath(self):
        return self.path

    def getFilename(self):
        return self.filename

    def setPath(self, path):
        self.path = path


    def setFilename(self, fn):
        self.filename = fn

