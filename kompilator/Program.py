class Program:
    def __init__(self, declarations, commands):
        self.declarations = declarations
        self.commands = commands

    
    def generateCode(self):
        result = []
        return result + ["HALT"]