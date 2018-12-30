from AbstractSyntaxTree.Expression import Expression

class NotArrayException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Identifier(Expression):
    def __init__(self, name, value):
        Expression.__init__(self, value)
        self.name = name