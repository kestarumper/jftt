from AbstractSyntaxTree.Expression import Expression

class BinaryOperator(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right