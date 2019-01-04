from Memory import manager as MemoryManager
import Instructions

class Identifier:
    def __init__(self, pidentifier):
        self.pidentifier = pidentifier
        MemoryManager.registerSymbol(pidentifier)

    @property
    def declaration(self):
        return MemoryManager.getDeclarationByPidentifier(self.pidentifier)

    def memAddressToReg(self, p, reg1, reg2):
        memoryId = MemoryManager.getBlockId(self.pidentifier)
        Instructions.setRegisterConst(p, reg1, memoryId)

class ArrayAccess(Identifier):
    def __init__(self, pidentifier, index):
        super(ArrayAccess, self).__init__(pidentifier)
        self.index = index

    def evalArrayOffsetToReg(self, p, reg):
        raise Exception("Not defined")

    def memAddressToReg(self, p, reg1, reg2):
        raise Exception("Not defined")

class ArrayAccessByNum(ArrayAccess):
    def __init__(self, pidentifier, num):
        super(ArrayAccessByNum, self).__init__(pidentifier, num)

    def memAddressToReg(self, p, reg1, reg2):
        declaration = self.declaration

        if not declaration.isArray():
            raise Exception("'%s' is not an Array" % declaration.pidentifier)

        memoryId = MemoryManager.getBlockId(self.pidentifier)
        print("INDEX", self.index)
        arrRangeFrom = declaration.rangeFrom
        arrRangeTo = declaration.rangeTo
        offset = self.index - arrRangeFrom
        if offset > arrRangeTo:
            raise Exception("Array out of bounds. Given %i, but range is (%i:%i)" % (self.index, arrRangeFrom, arrRangeTo))
        Instructions.setRegisterConst(p, reg2, offset)
        Instructions.setRegisterConst(p, reg1, memoryId)
        Instructions.ADD(p, reg1, reg2)

class ArrayAccessByPidentifier(ArrayAccess):
    def __init__(self, pidentifier, pid):
        super(ArrayAccessByPidentifier, self).__init__(pidentifier, pid)

    def memAddressToReg(self, p, reg1, reg2):
        declaration = self.declaration

        if not declaration.isArray():
            raise Exception("'%s' is not an Array" % declaration.pidentifier)

        memoryId = declaration.memoryId
        arrRangeFrom = declaration.rangeFrom
        arrRangeTo = declaration.rangeTo

        indexIdentifier = Identifier(self.index)

        # tab(5:15)         [memoryId:memoryId+10]
        # a := 7
        # tab(a)
        Instructions.LOAD_IDENTIFIER_VALUE_TO_REGISTER(p, indexIdentifier, reg2)  # reg2 = a.value
        Instructions.setRegisterConst(p, reg1, arrRangeFrom)                      # reg1 = arrRangeFrom
        Instructions.SUB(p, reg2, reg1)                                           # reg2 = reg2 - reg1 // offset
        Instructions.setRegisterConst(p, reg1, memoryId)                          # reg1 = memoryId
        Instructions.ADD(p, reg1, reg2)                                           # reg1 = reg1 + reg2 // memid + offset