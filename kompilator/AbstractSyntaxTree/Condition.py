import Instructions

class Condition:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def generateCode(self, p):
        if self.operator == '>':
            return Instructions.CONDITION_GT(p, self.left, self.right)
        if self.operator == '>=':
            return Instructions.CONDITION_GEQ(p, self.left, self.right)
        if self.operator == '<':
            return Instructions.CONDITION_LT(p, self.left, self.right)
        if self.operator == '<=':
            return Instructions.CONDITION_LEQ(p, self.left, self.right)
        if self.operator == '=':
            return Instructions.CONDITION_EQ(p, self.left, self.right)
        if self.operator == '!=':
            return Instructions.CONDITION_NEQ(p, self.left, self.right)
        else:
            raise Exception("Undefined CONDITION operator '%s'" % self.operator)