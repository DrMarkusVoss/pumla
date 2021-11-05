
class PUMLARelation:
    ''' store PUMLA relations '''
    def __init__(self, id, start, reltype, end, reltxt="", techntxt=""):
        self.id = id
        self.start = start
        self.end = end
        self.reltype = reltype
        self.reltxt = reltxt
        self.techntxt = techntxt
        self.path = "-"
        self.filename = "-"
        # tagged values is a dict are like
        # like {<tag>: [<tag_value1>, <tag_value2>, ...]}
        self.tagged_values = {}


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

    def getTechnTxt(self):
        return self.techntxt

    def getPath(self):
        return self.path

    def getFilename(self):
        return self.filename

    def setPath(self, path):
        self.path = path


    def setFilename(self, fn):
        self.filename = fn

    def getTaggedValues(self):
        return self.tagged_values

    def getTaggedValuesMRJSONFormat(self):
        tvs = []
        for k in self.tagged_values.keys():
            nd = {"tag": k, "values": self.tagged_values[k]}
            tvs.append(nd)

        return tvs

    def addTaggedValue(self, tag, value):
        """add a tagged value."""
        if (tag in self.tagged_values):
            self.tagged_values[tag].append(value)
        else:
            self.tagged_values[tag] = [value]

    def addValueToTag(self, value, tag):
        """add a value to a already existing tag."""
        self.tagged_values[tag].append(value)

