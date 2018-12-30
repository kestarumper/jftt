from AbstractSyntaxTree.Expression import Expression

class Condition(Expression):
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

    def get_value(self):
        # return Condition.operation[self.operator](self.left, self.right)
        return (self.left, self.operator, self.right)