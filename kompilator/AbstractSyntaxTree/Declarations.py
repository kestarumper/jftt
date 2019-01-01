from Memory import manager as MemoryManager

class DeclarationVariable:
    def __init__(self, pidentifier, isarr=False):
        self.pidentifier = pidentifier
        self.isarr = isarr

    def isArray(self):
        return self.isarr == True

    @property
    def memoryId(self):
        return MemoryManager.getBlockId(self.pidentifier)


class DeclarationArray(DeclarationVariable):
    def __init__(self, pidentifier, rangeFrom, rangeTo):
        super(DeclarationArray, self).__init__(pidentifier, True)
        self.rangeFrom = rangeFrom
        self.rangeTo = rangeTo