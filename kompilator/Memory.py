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

    def checkDuplicateDeclarations(self):
        for decl in self.declarations:
            pidentifier = decl.pidentifier
            if pidentifier in self.declaredPidentifiers:
                raise Exception("Duplicate declaration for '%s'" % pidentifier)
            self.declaredPidentifiers.add(pidentifier)

    # def checkIfAllSymbolsAreDeclared(self):
    #     symbols = self.getSymbols()
    #     declaredSymbols = self.declaredPidentifiers
    #     for sym in symbols:
    #         if sym not in declaredSymbols:
    #             raise Exception("Symbol '%s' not declared" % sym)

    def listDeclarationsMemory(self):
        print("DECLARATIONS:")
        print(self.declaredPidentifiers)
        print("MEMORY:")
        print(self.memmap)

    def unregister(self, declaration):
        try:
            del self.memmap[declaration.pidentifier]
            declaration.memoryId = None
        except KeyError as key:
            raise Exception("Trying to unregister not declared identifier %s" % key)

    def assignMem(self, declaration):
        pidentifier = declaration.pidentifier

        blockLength = 1
        if declaration.isArray():
            blockLength = declaration.length

        assignedMemoryBlockId = self.lastblockid
        
        self.memmap[pidentifier] = declaration
        declaration.memoryId = assignedMemoryBlockId

        self.lastblockid += blockLength

    def assignMemToDeclarations(self):
        for declaration in self.declarations:
            self.assignMem(declaration)

    def getUnnamedMemBlock(self):
        assignedMem = self.lastblockid
        self.lastblockid += 1
        return assignedMem

    # def registerSymbol(self, pidentifier):
    #     if pidentifier not in self.memmap:
    #         self.memmap[pidentifier] = None

    def getSymbols(self):
        return self.memmap.keys()

    def getBlockId(self, name):
        try:
            memoryId = self.memmap[name].memoryId
            if memoryId == None:
                raise Exception("Identifier '%s' has no memory allocated" % name)
            return memoryId
        except KeyError:
            raise Exception("Identifier '%s' is not declared in current context" % name)

    def getDeclarationByPidentifier(self, pid):
        decl = self.memmap[pid]
        if not decl:
            raise Exception("Declaration '%s' not found" % pid)
        return decl

manager = MemoryManager()