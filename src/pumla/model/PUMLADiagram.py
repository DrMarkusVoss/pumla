class PUMLAConnection:
    ''' store PUMLA diagram information '''
    def __init__(self, alias, title=""):
        self.alias = alias
        self.title = title
        self.path = "-"
        self.filename = "-"
        self.elements = []
        self.mainlayout = {"direction": "l-to-r"}
