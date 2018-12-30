from tokenizer import lexer, tokens
import ply.yacc as yacc
from AbstractSyntaxTree.Identifier import Identifier
from AbstractSyntaxTree.Pidentifier import Pidentifier
from AbstractSyntaxTree.Condition import Condition
from AbstractSyntaxTree.Value import Value
from AbstractSyntaxTree.BinaryOperator import BinaryOperator
from AbstractSyntaxTree.Number import Number
from AbstractSyntaxTree.ArrayAccess import ArrayAccessByNum, ArrayAccessByPidentifier

def DEBUG(obj):
    print("[DEBUG]")
    print(repr(obj))
    print("[DEBUGEND]")


def p_program(p):
    '''program      : DECLARE declarations IN commands END'''
    p[0] = (p[2], p[4])


def p_declarations(p):
    '''declarations : declarations pidentifier SEMI
                    | declarations pidentifier LPAREN num COLON num RPAREN SEMI
                    | '''


def p_commands(p):
    '''commands  : commands command
                 | command'''


def p_command(p):
    '''command  : identifier ASSIGN expression SEMI
                | IF condition THEN commands ELSE commands ENDIF
                | IF condition THEN commands ENDIF
                | WHILE condition DO commands ENDWHILE
                | DO commands WHILE condition ENDDO
                | FOR pidentifier FROM value TO value DO commands ENDFOR
                | FOR pidentifier FROM value DOWNTO value DO commands ENDFOR
                | READ identifier SEMI
                | WRITE value SEMI'''


def p_expression_value(p):
    '''expression   : value'''
    p[0] = Value(p[1])


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
    p[0] = Value(p[1])


def p_value_num(p):
    '''value    : num'''
    p[0] = Number(p[1])


def p_identifier(p):
    '''identifier   : pidentifier'''
    p[0] = Pidentifier(p[1])


def p_identifier_arrayAccess_pidentifier(p):
    '''identifier   : pidentifier LPAREN pidentifier RPAREN'''
    p[0] = ArrayAccessByPidentifier(p[1], p[3])


def p_identifier_arrayAccess_num(p):
    '''identifier   : pidentifier LPAREN num RPAREN'''
    p[0] = ArrayAccessByNum(p[1], p[3])


def p_error(p):
    raise SyntaxError("Syntax error")


parser = yacc.yacc()
