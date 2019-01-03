from tokenizer import lexer, tokens
import ply.yacc as yacc
from AbstractSyntaxTree.Condition import Condition
from AbstractSyntaxTree.Expression import ValueFromIdentifier, Number, Expression, Identifier, BinaryOperator
from AbstractSyntaxTree.ArrayAccess import ArrayAccessByNum, ArrayAccessByPidentifier
from AbstractSyntaxTree.Command import *
from AbstractSyntaxTree.Declarations import *
from Program import Program


def p_program(p):
    '''program      : DECLARE declarations IN commands END'''
    p[0] = Program(p[2], p[4])


def p_declarations_VARIABLE(p):
    '''declarations : declarations pidentifier SEMI'''
    if not p[1]:
        p[1] = []
    newVariable = DeclarationVariable(p[2])
    p[1].append(newVariable)
    p[0] = p[1]


def p_declarations_ARRAY(p):
    '''declarations : declarations pidentifier LPAREN num COLON num RPAREN SEMI'''
    if not p[1]:
        p[1] = []
    rangeFrom = p[4]
    rangeTo = p[6]
    pidentifier = p[2]
    newArray = DeclarationArray(pidentifier, rangeFrom, rangeTo)
    p[1].append(newArray)
    p[0] = p[1]


def p_declarations_EMPTY(p):
    '''declarations : '''
    p[0] = []


def p_commands_append(p):
    '''commands  : commands command'''
    if not p[1]:
        p[1] = []
    p[1].append(p[2])
    p[0] = p[1]


def p_commands(p):
    '''commands  : command'''
    p[0] = [p[1]]


def p_command_ASSIGN(p):
    '''command  : identifier ASSIGN expression SEMI'''
    p[0] = CommandAssign(p[1], p[3])


def p_command_IFTHENELSE(p):
    '''command  : IF condition THEN commands ELSE commands ENDIF'''
    p[0] = CommandIfThenElse(p[2], p[4], p[6])


def p_command_IFTHEN(p):
    '''command  : IF condition THEN commands ENDIF'''
    p[0] = CommandIfThen(p[2], p[4])


def p_command_WHILE(p):
    '''command  : WHILE condition DO commands ENDWHILE'''
    p[0] = CommandWhile(p[2], p[4])


def p_command_DOWHILE(p):
    '''command  : DO commands WHILE condition ENDDO'''
    p[0] = CommandDoWhile(p[2], p[4])


def p_command_FOR(p):
    '''command  : FOR pidentifier FROM value TO value DO commands ENDFOR'''
    p[0] = CommandForTo(p[2], p[4], p[6], p[8])


def p_command_FORDOWNTO(p):
    '''command  : FOR pidentifier FROM value DOWNTO value DO commands ENDFOR'''
    p[0] = CommandForDownto(p[2], p[4], p[6], p[8])


def p_command_READ(p):
    '''command  : READ identifier SEMI'''
    p[0] = CommandRead(p[2])


def p_command_WRITE(p):
    '''command  : WRITE value SEMI'''
    p[0] = CommandWrite(p[2])


def p_expression_value(p):
    '''expression   : value'''
    p[0] = p[1]


def p_expression(p):
    '''expression   : value PLUS value
                    | value MINUS value
                    | value TIMES value
                    | value DIVIDE value
                    | value MODULO value'''
    p[0] = BinaryOperator(left=p[1], operator=p[2], right=p[3])


def p_condition(p):
    '''condition    : value EQ value
                    | value NEQ value
                    | value LT value
                    | value GT value
                    | value LEQ value
                    | value GEQ value'''
    p[0] = Condition(left=p[1], operator=p[2], right=p[3])


def p_value_identifier(p):
    '''value    : identifier'''
    p[0] = ValueFromIdentifier(p[1])


def p_value_num(p):
    '''value    : num'''
    p[0] = Number(p[1])


def p_identifier(p):
    '''identifier   : pidentifier'''
    p[0] = Identifier(p[1])


def p_identifier_arrayAccess_pidentifier(p):
    '''identifier   : pidentifier LPAREN pidentifier RPAREN'''
    p[0] = ArrayAccessByPidentifier(p[1], p[3])


def p_identifier_arrayAccess_num(p):
    '''identifier   : pidentifier LPAREN num RPAREN'''
    p[0] = ArrayAccessByNum(p[1], p[3])


def p_error(p):
    raise SyntaxError("Syntax error %s" % p)


parser = yacc.yacc()
