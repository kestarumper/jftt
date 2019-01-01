from Memory import manager as MemoryManager


class Program:
    def __init__(self, declarations, commands):
        self.declarations = declarations
        self.commands = commands
        self.instructions = []
        self.counter = 0
        self.assignMemoryToDeclarations()
        self.processCommands()

    def getCounter(self):
        return self.counter

    def incCounter(self):
        self.counter += 1
        return self

    def assignMemoryToDeclarations(self):
        print([(decl.pidentifier, decl.memoryId) for decl in self.declarations])

    def makeInstr(self, instr, X, Y=""):
        instrStr = "%s %s %s" % (instr, X, Y)
        self.incCounter()
        return instrStr

    def processCommands(self):
        for com in self.commands:
            instrSet = com.generateCode(self)
            for instr in instrSet:
                self.instructions.append(instr)

    def generateCode(self):
        return '\n'.join(self.instructions + ["HALT"])
