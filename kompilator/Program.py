from Memory import manager as MemoryManager

class Program:
    def __init__(self, declarations, commands):
        self.declarations = declarations
        self.commands = commands
        self.assignMemoryToIdentifiers()

    def assignMemoryToIdentifiers(self):
        for declaration in self.declarations:
            MemoryManager.assignMem(declaration.pidentifier)
    
    def generateCode(self):
        result = []
        return result + ["HALT"]