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


class Future:
    def materialize(self, j):
        raise Exception("Materialize not defined for %s" % self.__class__)


class FutureJZERO(Future):
    def __init__(self, program, X):
        self.X = X
        self.program = program
        self.instrId = program.addFutureInstr(self)

    def materialize(self, j):
        self.program.instructions[self.instrId] = "%s %s %s" % ('JZERO', self.X, j)


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
    memoryId = identifier.memoryId
    GET(p, REG.B)
    setRegisterConst(p, REG.A, memoryId)
    STORE(p, REG.B)


def WRITE(p, value):
    value.evalToRegInstr(p, REG.B)
    p.makeInstr('PUT', REG.B)

# REGISTERS
# A - memory ID
# B - ACCUMULATOR / left operand
# C - right operand
# D - TEMP_COPY
# E
# F
# G
# H - CONDITION RESULT


def setRegisterConst(p, reg, val):
    clearRegister(p, reg)
    while val > 0:
        INC(p, reg)
        val -= 1


def ASSIGN(p, identifier, expression):
    memoryId = identifier.memoryId
    expression.evalToRegInstr(p, REG.B)
    setRegisterConst(p, REG.A, memoryId)
    STORE(p, REG.B)


def LOAD_MEM_TO_REG(p, memoryId, reg):
    setRegisterConst(p, REG.A, memoryId)
    LOAD(p, reg)


def LOAD_IDENTIFIER_VALUE_TO_REGISTER(p, identifier, reg):
    memoryId = identifier.memoryId
    LOAD_MEM_TO_REG(p, memoryId, reg)


def LOAD_NUMBER_VALUE_TO_REGISTER(p, number, reg):
    setRegisterConst(p, reg, number)


def PLUS(p, leftValue, rightValue, destReg=REG.B, helpReg=REG.C):
    if destReg == helpReg:
        raise Exception("Cannot use same registers")
    leftValue.evalToRegInstr(p, destReg)
    rightValue.evalToRegInstr(p, helpReg)
    ADD(p, destReg, helpReg)


def CONDITION_LT(p, leftVal, rightVal):
    leftVal.evalToRegInstr(p, REG.H)        # rH = left
    rightVal.evalToRegInstr(p, REG.C)       # rC = right
    SUB(p, REG.H, REG.C)                    # rH = max{rH - rC, 0}
                                            # rH == 0 = TRUE (left < right)
                                            # rH != 0 = FALSE (left >= right)

def CONDITION_GT(p, leftVal, rightVal):
    CONDITION_LT(p, rightVal, leftVal)


def CONDITION_EQ(p, leftVal, rightVal):
    leftVal.evalToRegInstr(p, REG.H)        # rH = left
    rightVal.evalToRegInstr(p, REG.C)       # rC = right
    COPY(p, REG.B, REG.H)                   # rB = rH
    SUB(p, REG.H, REG.C)                    # rH = max{rH - rC, 0}
    SUB(p, REG.C, REG.B)                    # rC = max{rC - rB, 0}
    ADD(p, REG.H, REG.C)                    # rH = rH + rC
                                            # 0 + 0 == TRUE (H == 0)
                                            # 1 + 0 v 0 + 1 == FALSE (H != 0)

def IF_THEN_ELSE(p, cond, thenCommands, elseCommands):
    cond.generateCode(p)

    fjzero = FutureJZERO(p, REG.H)
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
