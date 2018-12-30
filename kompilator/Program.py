from Memory import MemoryManager

class Program:
    def __init__(self, declarations, commands):
        self.memoryManager = MemoryManager()
        self.declarations = declarations
        self.commands = commands
        self.assignMemoryToIdentifiers()

    def assignMemoryToIdentifiers(self):
        for declaration in self.declarations:
            self.memoryManager.assignMem(declaration.pidentifier)
    
    def generateCode(self):
        result = []
        return result + ["HALT"]