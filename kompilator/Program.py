from Memory import MemoryManager

class Program:
    def __init__(self, declarations, commands):
        self.memoryManager = MemoryManager()
        self.declarations = declarations
        self.commands = commands
        self.instructions = []
        self.assignMemoryToDeclarations()
        self.processCommands()

    def assignMemoryToDeclarations(self):
        for declaration in self.declarations:
            self.memoryManager.assignMem(declaration.pidentifier)


    def processCommands(self):
        for com in self.commands:
            instructionSet = com.generateCode()
            for instr in instructionSet:
                self.instructions.append(instr)

    
    def generateCode(self):
        return '\n'.join(self.instructions + ["HALT"])