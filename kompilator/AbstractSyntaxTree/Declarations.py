class Declarations:
    def __init__(self, declaration):
        self.declarations = []
        if declaration:
            self.append(declaration)

    def append(self, declaration):
        self.declarations.append(declaration)
        return self


class DeclarationVariable:
    def __init__(self, pidentifier, isarr=False):
        self.memoryId = None
        self.pidentifier = pidentifier
        self.isarr = isarr

    def isArray(self):
        return self.isarr == True


class DeclarationArray(DeclarationVariable):
    def __init__(self, pidentifier, rangeFrom, rangeTo):
        super(DeclarationArray, self).__init__(pidentifier, True)
        self.rangeFrom = rangeFrom
        self.rangeTo = rangeTo