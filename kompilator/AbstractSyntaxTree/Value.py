from AbstractSyntaxTree.Expression import Expression

class Value(Expression):
    def __init__(self, value):
        super(Value, self).__init__(value)