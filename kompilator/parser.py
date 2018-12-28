from tokenizer import lexer, tokens
import ply.yacc as yacc


def p_program(p):
    '''program      : DECLARE declarations IN commands END'''
    p[0] = "TOP RULE"


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


def p_expression(p):
    '''expression   : value
                    | value PLUS value
                    | value MINUS value
                    | value TIMES value
                    | value DIVIDE value
                    | value MODULO value'''


def p_condition(p):
    '''condition    : value EQ value
                    | value NEQ value
                    | value LT value
                    | value GT value
                    | value LEQ value
                    | value GEQ value'''


def p_value(p):
    '''value    : num
                | identifier'''


def p_identifier(p):
    '''identifier   : pidentifier
                    | pidentifier LPAREN pidentifier RPAREN
                    | pidentifier LPAREN num RPAREN'''


def p_error(p):
    raise SyntaxError("Syntax error")

parser = yacc.yacc()
