class MemoryException(Exception):
    pass


class MemoryManager:
    def __init__(self):
        self.declarations = None
        self.declaredPidentifiers = set()
        self.memmap = {}
        self.lastblockid = 0

    def runMemCheck(self, declarations):
        self.declarations = declarations
        self.checkDuplicateDeclarations()
        self.checkIfAllSymbolsAreDeclared()

    def checkDuplicateDeclarations(self):
        for decl in self.declarations:
            pidentifier = decl.pidentifier
            if pidentifier in self.declaredPidentifiers:
                raise Exception("Duplicate declaration for '%s'" % pidentifier)
            self.declaredPidentifiers.add(pidentifier)

    def checkIfAllSymbolsAreDeclared(self):
        symbols = self.getSymbols()
        declaredSymbols = self.declaredPidentifiers
        for sym in symbols:
            if sym not in declaredSymbols:
                raise Exception("Symbol '%s' not declared" % sym)

    def listDeclarationsMemory(self):
        print("DECLARATIONS:")
        print(self.declaredPidentifiers)
        print("MEMORY:")
        print(self.memmap)

    def assignMem(self, declaration):
        pidentifier = declaration.pidentifier

        if pidentifier not in self.memmap:
            self.registerSymbol(pidentifier)

        if self.memmap[pidentifier] != None:
            raise Exception("Duplicate memory assignment for symbol '%s'" % pidentifier)

        blockLength = 1
        if declaration.isArray():
            blockLength = declaration.length

        assignedMemoryBlockId = self.lastblockid
        
        self.memmap[pidentifier] = assignedMemoryBlockId
        declaration.memoryId = assignedMemoryBlockId

        self.lastblockid += blockLength

    def assignMemToDeclarations(self):
        for declaration in self.declarations:
            self.assignMem(declaration)

    def registerSymbol(self, pidentifier):
        self.memmap[pidentifier] = None

    def getSymbols(self):
        return self.memmap.keys()

    def getBlockId(self, name):
        if not name in self.memmap:
            raise MemoryException("Identifier %s has no memory allocated" % name)
        return self.memmap[name]


manager = MemoryManager()