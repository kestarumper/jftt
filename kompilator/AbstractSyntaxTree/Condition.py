import Instructions

class Condition:
    operation = {
        "EQ": lambda l, r: (l, r),
        "NEQ": lambda l, r: (l, r),
        "LT": lambda l, r: (l, r),
        "GT": lambda l, r: (l, r),
        "LEQ": lambda l, r: (l, r),
        "GEQ": lambda l, r: (l, r),
    }

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def generateCode(self, p):
        if self.operator == '>':
            return Instructions.CONDITION_GT(p, self.left, self.right)
        if self.operator == '<':
            return Instructions.CONDITION_LT(p, self.left, self.right)
        if self.operator == '=':
            return Instructions.CONDITION_EQ(p, self.left, self.right)
        else:
            raise Exception("Undefined CONDITION operator '%s'" % self.operator)