import ply.lex as lex
import ply.yacc as yacc
import math
import sys

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'TIMES',
    'MODULO',
    "POWER",
    "LPAREN",
    "RPAREN",
    "COMMENT"
]

# t_COMMENT = r'\#(([a-zA-Z ]*?)|(([a-zA-Z ]*?)\\\n)+)([a-zA-Z ]*\n)'
t_COMMENT = r'\#.*'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'


def t_PLUS(t):
    r'\+'
    t.value = (t.value, lambda a, b: a + b)
    return t


def t_MINUS(t):
    r'-'
    t.value = (t.value, lambda a, b: a - b)
    return t


def t_TIMES(t):
    r'\*'
    t.value = (t.value, lambda a, b: a * b)
    return t


def t_DIVIDE(t):
    r'\/'
    t.value = (t.value, lambda a, b: a / b)
    return t


def t_POWER(t):
    r'\^'
    t.value = (t.value, lambda a, b: a ** b)
    return t


def t_MODULO(t):
    r'%'
    t.value = (t.value, lambda a, b: a % b)
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_error(t):
    raise SyntaxError("Nieprawidłowy znak '%s'" % t.value[0])


lexer = lex.lex()

# PARSER
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),
)


def p_statement(t):
    '''statement    : expression'''
    print(t[1][1])
    print("Wynik:\t", math.floor(t[1][0]))


def p_expression_binary(t):
    '''expression   : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression
                    | expression POWER expression
                    | expression MODULO expression'''
    t[0] = (t[2][1](t[1][0], t[3][0]),
            '{} {} {}'.format(t[1][1], t[3][1], t[2][0]))


def p_expression_parentheses(t):
    '''expression   : LPAREN expression RPAREN'''
    t[0] = t[2]


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = (-t[2][0], '{} -1 *'.format(t[2][1]))


def p_expression_number(t):
    '''expression   : NUMBER'''
    t[0] = (t[1], '{}'.format(t[1]))


def p_discard_comment(t):
    '''statement  : COMMENT'''
    pass


def p_error(t):
    raise SyntaxError("Błędna składnia")


def prCyan(skk): print("\033[96m{}\033[00m".format(skk))


def prRed(skk): print("\033[91m{}\033[00m".format(skk))


parser = yacc.yacc()

lines = [line for line in sys.stdin]
lines = ''.join(lines)
lines = lines.split('\\\n')
lines = ''.join(lines)
lines = lines.split('\n')


for line in lines:
    try:
        prCyan(line)
        parser.parse(line)
    except Exception as err:
        prRed(err)
    print('')
