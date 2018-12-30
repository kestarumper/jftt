from AbstractSyntaxTree.Identifier import Identifier

class Pidentifier(Identifier):
    def __init__(self, name):
        super(Pidentifier, self).__init__(name, None)