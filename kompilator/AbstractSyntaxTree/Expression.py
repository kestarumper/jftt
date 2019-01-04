import Instructions
from AbstractSyntaxTree.Identifier import ArrayAccess

class Expression:
    def evalToRegInstr(self, p, reg):
        raise Exception("evalToRegInstr() not defined for %s" % self.__class__)


class Number(Expression):
    def __init__(self, num):
        self.num = num

    def evalToRegInstr(self, p, reg):
        return Instructions.LOAD_NUMBER_VALUE_TO_REGISTER(p, self.num, reg)


class ValueFromIdentifier(Expression):
    def __init__(self, identifier):
        self.identifier = identifier

    def evalToRegInstr(self, p, reg):
        if isinstance(self.identifier, ArrayAccess):
            return Instructions.LOAD_ARRAY_VALUE_TO_REGISTER(p, self.identifier, reg)
        return Instructions.LOAD_IDENTIFIER_VALUE_TO_REGISTER(p, self.identifier, reg)


class BinaryOperator(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evalToRegInstr(self, p, reg):
        if self.operator == '+':
            return Instructions.PLUS(p, self.left, self.right, reg)
        if self.operator == '-':
            return Instructions.MINUS(p, self.left, self.right, reg)
        if self.operator == '*':
            return Instructions.TIMES(p, self.left, self.right, reg)
        if self.operator == '/':
            return Instructions.DIVIDE(p, self.left, self.right, reg)
        if self.operator == '%':
            return Instructions.MODULO(p, self.left, self.right, reg)
        else:
            raise Exception("Operator '%s' not defined" % self.operator)
