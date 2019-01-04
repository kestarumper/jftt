class ArrayAccess:
    def __init__(self, pidentifier, index):
        self.pidentifier = pidentifier
        self.index = index

class ArrayAccessByNum(ArrayAccess):
    def __init__(self, pidentifier, num):
        super(ArrayAccessByNum, self).__init__(pidentifier, num)

class ArrayAccessByPidentifier(ArrayAccess):
    def __init__(self, pidentifier, pid):
        super(ArrayAccessByPidentifier, self).__init__(pidentifier, pid)