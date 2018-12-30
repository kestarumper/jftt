class Command:
    pass


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
        self.identifier = identifier
        self.expression = expression


class CommandIfThen(Command):
    def __init__(self, condition, thenCommands):
        self.condition = condition
        self.thenCommands = thenCommands


class CommandIfThenElse(CommandIfThen):
    def __init__(self, condition, thenCommands, elseCommands):
        super(CommandIfThenElse, self).__init__(condition, thenCommands)
        self.elseCommands = elseCommands


class CommandWhile(Command):
    def __init__(self, condition, commands):
        self.condition = condition
        self.commands = commands


class CommandDoWhile(Command):
    def __init__(self, commands, condition):
        self.commands = commands
        self.condition = condition


class CommandForTo(Command):
    def __init__(self, pidentifier, fromValue, toValue, commands):
        self.pidentifier = pidentifier
        self.fromValue = fromValue
        self.toValue = toValue
        self.commands = commands


class CommandForDownto(CommandForTo):
    def __init__(self, pidentifier, fromValue, toValue, commands):
        super(CommandForDownto, self).__init__(pidentifier, fromValue, toValue, commands)

    
class CommandRead(Command):
    def __init__(self, identifier):
        self.identifier = identifier


class CommandWrite(Command):
    def __init__(self, value):
        self.value = value