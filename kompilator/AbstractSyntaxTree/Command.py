import Instructions
from AbstractSyntaxTree.Declarations import DeclarationVariable
from AbstractSyntaxTree.Identifier import Identifier

class Command:
    def __init__(self):
        pass

    def generateCode(self, program):
        raise Exception("generateCode() not defined for %s" % self.__class__)


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

    def generateCode(self, p):
        Instructions.IF_THEN(
            p, self.condition, self.thenCommands)


class CommandIfThenElse(CommandIfThen):
    def __init__(self, condition, thenCommands, elseCommands):
        super(CommandIfThenElse, self).__init__(condition, thenCommands)
        self.elseCommands = elseCommands

    def generateCode(self, p):
        Instructions.IF_THEN_ELSE(
            p, self.condition, self.thenCommands, self.elseCommands)


class CommandWhile(Command):
    def __init__(self, condition, commands):
        super(CommandWhile, self).__init__()
        self.condition = condition
        self.commands = commands

    def generateCode(self, p):
        return Instructions.WHILE(p, self.condition, self.commands)


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

    def generateCode(self, p):
        declaredIterator = DeclarationVariable(self.pidentifier, islocal=True)
        declaredIterator.register()
        iteratorIdentifier = Identifier(self.pidentifier)
        Instructions.FOR_TO(p, self.fromValue, self.toValue,
            iteratorIdentifier, self.commands)
        declaredIterator.delete()


class CommandForDownto(CommandForTo):
    def __init__(self, pidentifier, fromValue, toValue, commands):
        super(CommandForDownto, self).__init__(
            pidentifier, fromValue, toValue, commands)

    def generateCode(self, p):
        declaredIterator = DeclarationVariable(self.pidentifier, islocal=True)
        declaredIterator.register()
        iteratorIdentifier = Identifier(self.pidentifier)
        Instructions.FOR_DOWNTO(p, self.fromValue, self.toValue,
            iteratorIdentifier, self.commands)
        declaredIterator.delete()

class CommandRead(Command):
    def __init__(self, identifier):
        super(CommandRead, self).__init__()
        self.identifier = identifier

    def generateCode(self, p):
        Instructions.READ(p, self.identifier)


class CommandWrite(Command):
    def __init__(self, value):
        super(CommandWrite, self).__init__()
        self.value = value

    def generateCode(self, p):
        Instructions.WRITE(p, self.value)
