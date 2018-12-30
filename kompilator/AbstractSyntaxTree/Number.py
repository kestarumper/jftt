from AbstractSyntaxTree.Value import Value

class Number(Value):
    def __init__(self, value):
        Value.__init__(self, value)