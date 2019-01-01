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


def GET(p, reg):
    return [p.makeInstr('GET', reg)]


def STORE(p, reg):
    return [p.makeInstr('STORE', reg)]


def LOAD(p, reg):
    return [p.makeInstr('LOAD', reg)]


def INC(p, reg):
    return [p.makeInstr('INC', reg)]


def JUMP(p, k):
    return [p.makeInstr('JUMP', k)]


def SUB(p, X, Y):
    return [p.makeInstr('SUB', X, Y)]


def ADD(p, X, Y):
    return [p.makeInstr('ADD', X, Y)]


def clearRegister(p, reg):
    return SUB(p, reg, reg)


def READ(p, identifier):
    memoryId = identifier.memoryId
    instructions = []
    instructions += GET(p, REG.B)
    instructions += setRegisterConst(p, REG.A, memoryId)
    instructions += STORE(p, REG.B)
    return instructions


def WRITE(p, value):
    instructions = []
    instructions += value.evalToRegInstr(p, REG.B)
    instructions += [p.makeInstr('PUT', REG.B)]
    return instructions

# REGISTERS
# A - memory ID
# B - ACCUMULATOR
# C - right binary operator value


def setRegisterConst(p, reg, val):
    instructions = []
    instructions += clearRegister(p, reg)
    while val > 0:
        instructions += INC(p, reg)
        val -= 1
    return instructions


def ASSIGN(p, identifier, expression):
    memoryId = identifier.memoryId
    instructions = []
    instructions += expression.evalToRegInstr(p, REG.B)
    instructions += setRegisterConst(p, REG.A, memoryId)
    instructions += STORE(p, REG.B)
    return instructions


def LOAD_MEM_TO_REG(p, memoryId, reg):
    instructions = []
    instructions += setRegisterConst(p, REG.A, memoryId)
    instructions += LOAD(p, reg)
    return instructions


def LOAD_IDENTIFIER_VALUE_TO_REGISTER(p, identifier, reg):
    memoryId = identifier.memoryId
    return LOAD_MEM_TO_REG(p, memoryId, reg)


def LOAD_NUMBER_VALUE_TO_REGISTER(p, number, reg):
    return setRegisterConst(p, reg, number)


def PLUS(p, leftValue, rightValue, destReg=REG.B, helpReg=REG.C):
    instructions = []
    if destReg == helpReg:
        raise Exception("Cannot use same registers")
    instructions += leftValue.evalToRegInstr(p, destReg)
    instructions += rightValue.evalToRegInstr(p, helpReg)
    instructions += ADD(p, destReg, helpReg)
    return instructions