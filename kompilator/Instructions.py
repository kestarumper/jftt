# GET X pobraną liczbę zapisuje w rejestrze rX oraz k ← k + 1 100
# PUT X wyświetla zawartość rejestru rX oraz k ← k + 1 100
# LOAD X rX ← prA oraz k ← k + 1 50
# STORE X prA ← rX oraz k ← k + 1 50
# COPY X Y rX ← rY oraz k ← k + 1 5
# ADD X Y rX ← rX + rY oraz k ← k + 1 5
# SUB X Y rX ← max{rX − rY , 0} oraz k ← k + 1 5
# HALF X rX ← brX/2c oraz k ← k + 1 1
# INC X rX ← rX + 1 oraz k ← k + 1 1
# DEC X rX ← max(rX − 1, 0) oraz k ← k + 1 1
# JUMP j k ← j 1
# JZERO X j jeśli rX = 0 to k ← j, w p.p. k ← k + 1 1
# JODD X j jeśli rX nieparzyste to k ← j, w p.p. k ← k + 1 1
# HALT zatrzymaj program 0

from Register import REG
from AbstractSyntaxTree.Command import CommandForTo
from AbstractSyntaxTree.Identifier import ArrayAccess
from Memory import manager as MemoryManager


class Future:
    def materialize(self, j):
        raise Exception("Materialize not defined for %s" % self.__class__)


class FutureJZERO(Future):
    def __init__(self, program, X):
        self.X = X
        self.program = program
        self.instrId = program.addFutureInstr(self)

    def materialize(self, j):
        self.program.instructions[self.instrId] = "%s %s %s" % (
            'JZERO', self.X, j)


class FutureJODD(Future):
    def __init__(self, program, X):
        self.X = X
        self.program = program
        self.instrId = program.addFutureInstr(self)

    def materialize(self, j):
        self.program.instructions[self.instrId] = "%s %s %s" % (
            'JODD', self.X, j)


class FutureJUMP(Future):
    def __init__(self, program):
        self.program = program
        self.instrId = program.addFutureInstr(self)

    def materialize(self, j):
        self.program.instructions[self.instrId] = "%s %s" % ('JUMP', j)


def GET(p, reg):
    p.makeInstr('GET', reg)


def STORE(p, reg):
    p.makeInstr('STORE', reg)


def LOAD(p, reg):
    p.makeInstr('LOAD', reg)


def INC(p, reg):
    p.makeInstr('INC', reg)


def JUMP(p, j):
    p.makeInstr('JUMP', j)


def DEC(p, X):
    p.makeInstr('DEC', X)


def HALF(p, X):
    p.makeInstr('HALF', X)


def SUB(p, X, Y):
    p.makeInstr('SUB', X, Y)


def JZERO(p, X, j):
    p.makeInstr('JZERO', X, j)


def ADD(p, X, Y):
    p.makeInstr('ADD', X, Y)


def COPY(p, X, Y):
    p.makeInstr('COPY', X, Y)


def clearRegister(p, reg):
    SUB(p, reg, reg)


def READ(p, identifier):
    identifier.memAddressToReg(p, REG.A, REG.B)
    GET(p, REG.B)
    STORE(p, REG.B)


def WRITE(p, value):
    value.evalToRegInstr(p, REG.B)
    p.makeInstr('PUT', REG.B)


def setRegisterConst(p, reg, val):
    clearRegister(p, reg)

    binVal = bin(val)[2:]   # number to binary representation
    length = len(binVal)    # how many digits
    for i, digit in enumerate(binVal):
        if digit == '1':
            INC(p, reg)         # reg = reg + 1
        if i < length - 1:
            ADD(p, reg, reg)    # reg = reg << 1


def ASSIGN(p, identifier, expression):
    decl = identifier.declaration
    if decl.islocal:
        raise Exception("Trying to modify local variable '%s'" % decl.pidentifier)
    if not isinstance(identifier, ArrayAccess) and decl.isarr == True:
        raise Exception("'%s' is an array, but used as normal variable" % decl.pidentifier)
    expression.evalToRegInstr(p, REG.B)
    identifier.memAddressToReg(p, REG.A, REG.C)
    STORE(p, REG.B)


def LOAD_IDENTIFIER_VALUE_TO_REGISTER(p, identifier, reg):
    decl = identifier.declaration;
    if reg == REG.A:
        raise Exception("Registers collision '%s'" % reg)
    if decl.isarr == True:
        raise Exception("'%s' is an array, but accessed as normal variable" % decl.pidentifier)
    identifier.memAddressToReg(p, REG.A, reg)
    LOAD(p, reg)


def LOAD_ARRAY_VALUE_TO_REGISTER(p, identifier, reg):
    identifier.memAddressToReg(p, REG.A, reg)
    LOAD(p, reg)


def LOAD_NUMBER_VALUE_TO_REGISTER(p, number, reg):
    setRegisterConst(p, reg, number)


def PLUS(p, leftValue, rightValue, destReg=REG.B, helpReg=REG.C):
    if destReg == helpReg:
        raise Exception("Cannot use same registers")
    leftValue.evalToRegInstr(p, destReg)
    rightValue.evalToRegInstr(p, helpReg)
    ADD(p, destReg, helpReg)


def MINUS(p, leftValue, rightValue, destReg=REG.B, helpReg=REG.C):
    if destReg == helpReg:
        raise Exception("Cannot use same registers")
    leftValue.evalToRegInstr(p, destReg)
    rightValue.evalToRegInstr(p, helpReg)
    SUB(p, destReg, helpReg)


def TIMES(p, leftValue, rightValue, destReg=REG.B, leftReg=REG.C, rightReg=REG.D):
    leftValue.evalToRegInstr(p, leftReg)
    rightValue.evalToRegInstr(p, rightReg)

    #TODO: JUMP IF ZERO LEFT or RIGHT

    # SWAP TO LEFT REGISTER BIGGER NUMBER
    COPY(p, destReg, rightReg)
    SUB(p, destReg, leftReg)
    fJUMP_SWAP = FutureJZERO(p, destReg)
    COPY(p, destReg, leftReg)
    COPY(p, leftReg, rightReg)
    COPY(p, rightReg, destReg)
    LABEL_AFTER_SWAP = p.getCounter()
    fJUMP_SWAP.materialize(LABEL_AFTER_SWAP)
    # END SWAP

    clearRegister(p, destReg)   # RESET c

    LABEL_LOOP = p.getCounter()
    fJUMP_TO_END = FutureJZERO(p, leftReg)
    fJUMP_TO_ADD = FutureJODD(p, leftReg)
    fJUMP_SHIFT = FutureJUMP(p)

    LABEL_ADD = p.getCounter()
    ADD(p, destReg, rightReg)

    LABEL_SHIFT = p.getCounter()
    HALF(p, leftReg)
    SHIFT_LEFT(p, rightReg)
    fJUMP_TO_LOOP = FutureJUMP(p)

    LABEL_END = p.getCounter()

    fJUMP_TO_END.materialize(LABEL_END)
    fJUMP_TO_ADD.materialize(LABEL_ADD)
    fJUMP_SHIFT.materialize(LABEL_SHIFT)
    fJUMP_TO_LOOP.materialize(LABEL_LOOP)


def SHIFT_LEFT(p, reg):
    ADD(p, reg, reg)


# REGISTERS
# A - memory ID
# B - ACCUMULATOR / left operand
# C - right operand
# D - Temp
# E - Temp
# F - Temp
def DIVIDE(p, numeratorVal, denominatorVal, REG_RESULT=REG.B, REG_REMAIN=REG.C, modulo=False):
    if modulo:
        REG_RESULT, REG_REMAIN = REG_REMAIN, REG_RESULT

    if REG_RESULT in [REG.A, REG.D, REG.E, REG_REMAIN] or REG_REMAIN in [REG.A, REG.D, REG.E, REG_RESULT]:
        raise Exception("Register collision in DIVISION")

    REG_SCALEDDIVISOR = REG.E
    REG_MULTIPLE = REG.F
    REG_TEMP = REG.G

    clearRegister(p, REG_RESULT)                     # result = 0

	# uint_type scaled_divisor = divisor;  // The right-hand side of division
    denominatorVal.evalToRegInstr(p, REG_SCALEDDIVISOR)
    # if(divisor == 0) {
	#     return;
	# }
    fJUMP_DIVISION_BY_ZERO = FutureJZERO(p, REG_SCALEDDIVISOR)

    setRegisterConst(p, REG_MULTIPLE, 1)             # multiple = 1
    numeratorVal.evalToRegInstr(p, REG_REMAIN)       # remain = dividend

    '''
    while(scaled_divisor < dividend)
	{
	    scaled_divisor = scaled_divisor + scaled_divisor; // Multiply by two.
	    multiple       = multiple       + multiple;       // Multiply by two.
	}
    '''
    LABEL_WHILE_CONDITION = p.getCounter()
    COPY(p, REG_TEMP, REG_REMAIN)
    SUB(p, REG_TEMP, REG_SCALEDDIVISOR)
    fJUMP_WHILE_END = FutureJZERO(p, REG_TEMP)
    SHIFT_LEFT(p, REG_SCALEDDIVISOR)
    SHIFT_LEFT(p, REG_MULTIPLE)
    fJUMP_WHILE_COND = FutureJUMP(p)
    LABEL_WHILE_END = p.getCounter()
    '''	
	do {
	    if(scaled_divisor <= remain)
	    {
	        remain = remain - scaled_divisor;
	        result = result + multiple;
	    }
	    scaled_divisor = scaled_divisor >> 1; // Divide by two.
	    multiple       = multiple       >> 1;
	} while(multiple != 0);
    '''
    LABEL_DO_WHILE_BEGIN = p.getCounter()

    COPY(p, REG_TEMP, REG_SCALEDDIVISOR)
    SUB(p, REG_TEMP, REG_REMAIN)
    fJUMP_IF = FutureJZERO(p, REG_TEMP)
    fJUMP_FALSE = FutureJUMP(p)
    # THEN BLOCK
    thenBlockStartLabel = p.getCounter()
    SUB(p, REG_REMAIN, REG_SCALEDDIVISOR)
    ADD(p, REG_RESULT, REG_MULTIPLE)
    thenBLockEndLabel = p.getCounter()
    # THEN END BLOCK

    HALF(p, REG_SCALEDDIVISOR)
    HALF(p, REG_MULTIPLE)

    fJUMP_DO_WHILE_CONDITION_FALSE = FutureJZERO(p, REG_MULTIPLE)
    fJUMP_DO_WHILE_BEGIN = FutureJUMP(p)


    LABEL_END = p.getCounter()
    fJUMP_DO_WHILE_CONDITION_FALSE.materialize(LABEL_END)
    fJUMP_IF.materialize(thenBlockStartLabel)
    fJUMP_FALSE.materialize(thenBLockEndLabel)
    fJUMP_DO_WHILE_BEGIN.materialize(LABEL_DO_WHILE_BEGIN)
    fJUMP_WHILE_COND.materialize(LABEL_WHILE_CONDITION)
    fJUMP_WHILE_END.materialize(LABEL_WHILE_END)
    fJUMP_DIVISION_BY_ZERO.materialize(LABEL_END)


def MODULO(p, value, mod, destReg):
    DIVIDE(p, value, mod, destReg, REG.C, modulo=True)


def CONDITION_LT(p, leftVal, rightVal):
    leftVal.evalToRegInstr(p, REG.B)        # rH = left
    rightVal.evalToRegInstr(p, REG.C)       # rC = right
    INC(p, REG.B)
    SUB(p, REG.B, REG.C)                    # rH = max{rH - rC, 0}
    # rH == 0 = TRUE (left < right)
    # rH != 0 = FALSE (left >= right)


def CONDITION_LEQ(p, leftVal, rightVal):
    leftVal.evalToRegInstr(p, REG.B)        # rH = left
    rightVal.evalToRegInstr(p, REG.C)       # rC = right
    SUB(p, REG.B, REG.C)                    # rH = max{rH - rC, 0}
    # rH == 0 = TRUE (left <= right)
    # rH != 0 = FALSE (left > right)


def CONDITION_GT(p, leftVal, rightVal):
    CONDITION_LT(p, rightVal, leftVal)      # inverted less than


def CONDITION_GEQ(p, leftVal, rightVal):
    CONDITION_LEQ(p, rightVal, leftVal)     # inverted less or equal


def CONDITION_EQ(p, leftVal, rightVal):
    leftVal.evalToRegInstr(p, REG.B)        # rB = left
    rightVal.evalToRegInstr(p, REG.C)       # rC = right
    COPY(p, REG.D, REG.B)                   # rD = rB
    SUB(p, REG.B, REG.C)                    # rB = max{rB - rC, 0}
    SUB(p, REG.C, REG.D)                    # rC = max{rC - rD, 0}
    ADD(p, REG.B, REG.C)                    # rB = rB + rC
    # 0 + 0 == TRUE (B == 0)
    # 1 + 0 v 0 + 1 == FALSE (B != 0)


def CONDITION_NEQ(p, leftVal, rightVal):
    CONDITION_EQ(p, leftVal, rightVal)
    fJUMP_IF_EQUAL = FutureJZERO(p, REG.B)
    clearRegister(p, REG.B)         # if B != 0 ==> B = TRUE
    fJUMP_SKIP = FutureJUMP(p)

    LABEL_EQUAL = p.getCounter()
    INC(p, REG.B)                   # if B == 0 ==> B = FALSE

    LABEL_NOT_EQUAL = p.getCounter()

    fJUMP_IF_EQUAL.materialize(LABEL_EQUAL)
    fJUMP_SKIP.materialize(LABEL_NOT_EQUAL)


def IF_THEN_ELSE(p, cond, thenCommands, elseCommands):
    cond.generateCode(p)

    fjzero = FutureJZERO(p, REG.B)
    # ELSE BLOCK
    for com in elseCommands:
        com.generateCode(p)
    fjump = FutureJUMP(p)
    # ELSE END BLOCK

    # THEN BLOCK
    thenBlockStartLabel = p.getCounter()
    for com in thenCommands:
        com.generateCode(p)
    thenBLockEndLabel = p.getCounter()
    # THEN END BLOCK

    fjzero.materialize(thenBlockStartLabel)
    fjump.materialize(thenBLockEndLabel)


def IF_THEN(p, cond, thenCommands):
    cond.generateCode(p)

    fjzero = FutureJZERO(p, REG.B)
    fjump = FutureJUMP(p)
    # THEN BLOCK
    thenBlockStartLabel = p.getCounter()
    for com in thenCommands:
        com.generateCode(p)
    thenBLockEndLabel = p.getCounter()
    # THEN END BLOCK

    fjzero.materialize(thenBlockStartLabel)
    fjump.materialize(thenBLockEndLabel)


def WHILE(p, cond, commands):
    LABEL_WHILE_CONDITION = p.getCounter()
    cond.generateCode(p)                        # CONDITION
    fJumpIntoWhile = FutureJZERO(p, REG.B)      # ENTER WHILE IF TRUE
    fJumpOutOfWhile = FutureJUMP(p)             # LEAVE WHILE IF FALSE
    LABEL_WHILE_INSIDE = p.getCounter()
    for com in commands:                        # WHILE BODY COMMANDS
        com.generateCode(p)
    fJumpLoop = FutureJUMP(p)                   # BACK TO CONDITION CHECK
    LABEL_WHILE_END = p.getCounter()            # ENDWHILE

    fJumpIntoWhile.materialize(LABEL_WHILE_INSIDE)
    fJumpOutOfWhile.materialize(LABEL_WHILE_END)
    fJumpLoop.materialize(LABEL_WHILE_CONDITION)


def DO_WHILE(p, cond, commands):
    LABEL_WHILE_INSIDE = p.getCounter()
    for com in commands:                        # WHILE BODY COMMANDS
        com.generateCode(p)
    cond.generateCode(p)                        # CONDITION
    fJumpIntoWhile = FutureJZERO(p, REG.B)      # ENTER WHILE IF TRUE

    fJumpIntoWhile.materialize(LABEL_WHILE_INSIDE)


def FOR_TO(p, rangeFromValue, rangeToValue, identifier, commands):
    '''
    A - memory address
    H - Iterator
    '''

    # i = rangeFfrom
    rangeFromValue.evalToRegInstr(p, REG.B)
    identifier.memAddressToReg(p, REG.A, None)
    STORE(p, REG.B)

    # make copy of rangeTo
    rangeToValue.evalToRegInstr(p, REG.H)
    rangeToValueMemBlockCopy = MemoryManager.getUnnamedMemBlock()
    setRegisterConst(p, REG.A, rangeToValueMemBlockCopy)
    STORE(p, REG.H)

    INC(p, REG.H)
    SUB(p, REG.H, REG.B)    # tyle razy ma sie wykonać

    LABEL_LOOP = p.getCounter()
    fJUMP_TO_END_IF_ITERATOR_IS_ZERO = FutureJZERO(p, REG.H)

    for com in commands:
        com.generateCode(p)
        if isinstance(com, CommandForTo):
            # restore count loop if there are nested FORs
            identifier.memAddressToReg(p, REG.A, None)
            LOAD(p, REG.B)

            setRegisterConst(p, REG.A, rangeToValueMemBlockCopy)
            LOAD(p, REG.H)

            INC(p, REG.H)
            SUB(p, REG.H, REG.B)

    DEC(p, REG.H)   # rH = rH - 1

    # rB = rangeTo
    setRegisterConst(p, REG.A, rangeToValueMemBlockCopy)
    LOAD(p, REG.B)

    INC(p, REG.B)
    identifier.memAddressToReg(p, REG.A, None)
    SUB(p, REG.B, REG.H)
    STORE(p, REG.B)

    fJUMP_LOOP = FutureJUMP(p)
    LABEL_END_FOR = p.getCounter()

    fJUMP_TO_END_IF_ITERATOR_IS_ZERO.materialize(LABEL_END_FOR)
    fJUMP_LOOP.materialize(LABEL_LOOP)


def FOR_DOWNTO(p, rangeFromValue, rangeToValue, identifier, commands):
    '''
    A - memory address
    H - Iterator
    '''

    # make copy of rangeTo
    rangeToValue.evalToRegInstr(p, REG.B)
    rangeToValueMemBlockCopy = MemoryManager.getUnnamedMemBlock()
    setRegisterConst(p, REG.A, rangeToValueMemBlockCopy)
    STORE(p, REG.B)

    rangeFromValue.evalToRegInstr(p, REG.H)
    identifier.memAddressToReg(p, REG.A, None)
    STORE(p, REG.H)                                             # i = FROM

    INC(p, REG.H)
    SUB(p, REG.H, REG.B)                                        # loop count

    LABEL_LOOP = p.getCounter()
    fJUMP_TO_END_IF_ITERATOR_IS_ZERO = FutureJZERO(
        p, REG.H)    # jump if rH == 0 ?

    for com in commands:
        com.generateCode(p)
        if isinstance(com, CommandForTo):
            # restore count loop if there are nested FORs
            identifier.memAddressToReg(p, REG.A, None)
            LOAD(p, REG.H)
            INC(p, REG.H)

            setRegisterConst(p, REG.A, rangeToValueMemBlockCopy)
            LOAD(p, REG.B)

            SUB(p, REG.H, REG.B)

    DEC(p, REG.H)                                               # rH := rH - 1

    # rB = rangeTo
    setRegisterConst(p, REG.A, rangeToValueMemBlockCopy)
    LOAD(p, REG.B)

    identifier.memAddressToReg(p, REG.A, None)
    ADD(p, REG.B, REG.H)
    DEC(p, REG.B)
    STORE(p, REG.B)

    fJUMP_LOOP = FutureJUMP(p)
    LABEL_END_FOR = p.getCounter()

    fJUMP_TO_END_IF_ITERATOR_IS_ZERO.materialize(LABEL_END_FOR)
    fJUMP_LOOP.materialize(LABEL_LOOP)
