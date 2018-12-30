class Command:
    def __init__(self):
        self.instructions = []

    def generateCode(self):
        return self.instructions

    def addInstruction(self, instr, X, Y=""):
        instruction = "%s %s %s" % (instr, X, Y)
        self.instructions.append(instruction)


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


class CommandIfThen(Command):
    def __init__(self, condition, thenCommands):
        super(CommandIfThen, self).__init__()
        self.condition = condition
        self.thenCommands = thenCommands


class CommandIfThenElse(CommandIfThen):
    def __init__(self, condition, thenCommands, elseCommands):
        super(CommandIfThenElse, self).__init__(condition, thenCommands)
        self.elseCommands = elseCommands


class CommandWhile(Command):
    def __init__(self, condition, commands):
        super(CommandWhile, self).__init__()
        self.condition = condition
        self.commands = commands


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


class CommandWrite(Command):
    def __init__(self, value):
        super(CommandWrite, self).__init__()
        self.value = value
