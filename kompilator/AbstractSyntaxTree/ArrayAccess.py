from AbstractSyntaxTree.Identifier import Identifier

class ArrayAccess(Identifier):
    def __init__(self, name, index):
        super(ArrayAccess, self).__init__(name, None)
        self.index = index

class ArrayAccessByNum(ArrayAccess):
    def __init__(self, name, num):
        super(ArrayAccessByNum, self).__init__(name, num)

class ArrayAccessByPidentifier(ArrayAccess):
    def __init__(self, name, pid):
        super(ArrayAccessByPidentifier, self).__init__(name, pid)