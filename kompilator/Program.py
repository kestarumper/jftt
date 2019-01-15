from Memory import manager as MemoryManager

class Program:
    def __init__(self, declarations, commands):
        self.declarations = declarations
        self.commands = commands
        self.instructions = []
        self.counter = 0
        MemoryManager.runMemCheck(self.declarations)
        MemoryManager.assignMemToDeclarations()
        self.processCommands()

    def getCounter(self):
        return self.counter

    def incCounter(self):
        self.counter += 1
        return self

    def addFutureInstr(self, future):
        self.incCounter()
        self.instructions.append(future)
        return self.counter - 1

    def makeInstr(self, instr, X, Y=""):
        instrStr = "%s %s %s" % (instr, X, Y)
        self.incCounter()
        self.instructions.append(instrStr)

    def processCommands(self):
        for com in self.commands:
            com.generateCode(self)

    def generateCode(self):
        return '\n'.join(self.instructions + ["HALT"])
