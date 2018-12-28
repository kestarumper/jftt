from tokenizer import lexer, tokens
import ply.yacc as yacc


def p_program(p):
    '''program      : DECLARE declarations IN commands END'''
    print("TOP RULE")


def p_declarations(p):
    '''declarations : declarations pidentifier;
                    | declarations pidentifier(num:num);
                    | '''


def p_commands(p):
    '''commands  : commands command
                 | command'''


def p_command(p):
    '''command  : identifier := expression;
                | IF condition THEN commands ELSE commands ENDIF
                | IF condition THEN commands ENDIF
                | WHILE condition DO commands ENDWHILE
                | DO commands WHILE condition ENDDO
                | FOR pidentifier FROM value TO value DO commands ENDFOR
                | FOR pidentifier FROM value DOWNTO value DO commands ENDFOR
                | READ identifier;
                | WRITE value;'''


def p_expression(p):
    '''expression   : value
                    | value + value
                    | value - value
                    | value * value
                    | value / value
                    | value % value'''


def p_condition(p):
    '''condition    : value = value
                | value != value
                | value < value
                | value > value
                | value <= value
                | value >= value'''


def p_value(p):
    '''value     : num
                | identifier'''


def p_identifier(p):
    '''identifier   : pidentifier
                    | pidentifier(pidentifier)
                    | pidentifier(num)'''


parser = yacc.yacc()
