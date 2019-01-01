import Instructions

class Command:
    def __init__(self):
        pass

    def generateCode(self, program):
        raise Exception("generateCode() not defined for %s" % self.__class__)


class Commands:
    def __init__(self, command):
        self.commands = []
        if command:
            self.append(command)

    def append(self, command):
        self.commands.append(command)
        return self


class CommandAssign(Command):
    def __init__(self, identifier, expression):
        super(CommandAssign, self).__init__()
        self.identifier = identifier
        self.expression = expression

    def generateCode(self, p):
        return Instructions.ASSIGN(p, self.identifier, self.expression)

class CommandIfThen(Command):
    def __init__(self, condition, thenCommands):
        super(CommandIfThen, self).__init__()
        self.condition = condition
        self.thenCommands = thenCommands


class CommandIfThenElse(CommandIfThen):
    def __init__(self, condition, thenCommands, elseCommands):
        super(CommandIfThenElse, self).__init__(condition, thenCommands)
        self.elseCommands = elseCommands

    def generateCode(self, p):
        instructions = []
        for com in self.elseCommands:
            instructions += com.generateCode(p)
        return instructions

class CommandWhile(Command):
    def __init__(self, condition, commands):
        super(CommandWhile, self).__init__()
        self.condition = condition
        self.commands = commands.commands

    def generateCode(self, p):
        instructions = []
        beforeCtr = p.getCounter()
        for com in self.commands:
            instructions += com.generateCode(p)
        afterCtr = p.getCounter()
        return instructions

class CommandDoWhile(Command):
    def __init__(self, commands, condition):
        super(CommandDoWhile, self).__init__()
        self.commands = commands
        self.condition = condition


class CommandForTo(Command):
    def __init__(self, pidentifier, fromValue, toValue, commands):
        super(CommandForTo, self).__init__()
        self.pidentifier = pidentifier
        self.fromValue = fromValue
        self.toValue = toValue
        self.commands = commands


class CommandForDownto(CommandForTo):
    def __init__(self, pidentifier, fromValue, toValue, commands):
        super(CommandForDownto, self).__init__(
            pidentifier, fromValue, toValue, commands)


class CommandRead(Command):
    def __init__(self, identifier):
        super(CommandRead, self).__init__()
        self.identifier = identifier

    def generateCode(self, p):
        return Instructions.READ(p, self.identifier)


class CommandWrite(Command):
    def __init__(self, value):
        super(CommandWrite, self).__init__()
        self.value = value

    def generateCode(self, p):
        return Instructions.WRITE(p, self.value)
