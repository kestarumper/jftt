from Memory import manager as MemoryManager

class DeclarationVariable:
    def __init__(self, pidentifier, isarr = False):
        self.memoryId = None
        self.pidentifier = pidentifier
        self.isarr = isarr
        self.length = 1

    def isArray(self):
        return self.isarr == True

class DeclarationArray(DeclarationVariable):
    def __init__(self, pidentifier, rangeFrom, rangeTo):
        super(DeclarationArray, self).__init__(pidentifier, True)
        if rangeFrom >= rangeTo:
            raise Exception("Bad array range (%i:%i)" % (rangeFrom, rangeTo))
        self.rangeFrom = rangeFrom
        self.rangeTo = rangeTo
        self.length = rangeTo - rangeFrom + 1