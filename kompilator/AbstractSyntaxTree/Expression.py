from Memory import manager as MemoryManager
import Instructions

class Expression:
    def evalToRegInstr(self, p, reg):
        raise Exception("evalToRegInstr() not defined for %s" % self.__class__)


class Number(Expression):
    def __init__(self, value):
        self.value = value


class ValueFromIdentifier(Expression):
    def __init__(self, identifier):
        self.identifier = identifier

    def evalToRegInstr(self, p, reg):
        return Instructions.LOAD_IDENTIFIER_VALUE_TO_REGISTER(p, self.identifier, reg)

    
class Identifier:
    def __init__(self, pidentifier):
        self.pidentifier = pidentifier
        self.memoryId = MemoryManager.assignMem(self)


class BinaryOperator(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evalToRegInstr(self, p, reg):
        return Instructions.PLUS(p, self.left, self.right, reg)