class ArrayAccess:
    def __init__(self, name, index):
        self.name = name
        self.index = index

class ArrayAccessByNum(ArrayAccess):
    def __init__(self, name, num):
        super(ArrayAccessByNum, self).__init__(name, num)

class ArrayAccessByPidentifier(ArrayAccess):
    def __init__(self, name, pid):
        super(ArrayAccessByPidentifier, self).__init__(name, pid)