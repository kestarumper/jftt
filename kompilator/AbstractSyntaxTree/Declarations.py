from Memory import manager as MemoryManager

class DeclarationVariable:
    def __init__(self, pidentifier, isarr = False, islocal = False, lineNumber = -1):
        self.lineNumber = lineNumber
        self.memoryId = None
        self.pidentifier = pidentifier
        self.isarr = isarr
        self.length = 1
        self.islocal = islocal

    def delete(self):
        MemoryManager.unregister(self)

    def register(self):
        MemoryManager.assignMem(self)

    def isArray(self):
        return self.isarr == True

    def __repr__(self):
        return str((self.memoryId, self.length, "Array" if self.isarr else "Var" ))

class DeclarationArray(DeclarationVariable):
    def __init__(self, pidentifier, rangeFrom, rangeTo, line):
        super(DeclarationArray, self).__init__(pidentifier, True, lineNumber=line)
        if rangeFrom > rangeTo:
            raise Exception("Bad array range %s(%i:%i) at line %i" % (pidentifier, rangeFrom, rangeTo, line))
        self.rangeFrom = rangeFrom
        self.rangeTo = rangeTo
        self.length = rangeTo - rangeFrom + 1