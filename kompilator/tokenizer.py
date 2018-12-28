import ply.lex as lex
from ply.lex import TOKEN

reserved = {
    'DECLARE': 'DECLARE',
    'IN': 'IN',
    'END': 'END',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'ENDIF': 'ENDIF',
    'DO': 'DO',
    'WHILE': 'WHILE',
    'ENDWHILE': 'ENDWHILE',
    'ENDDO': 'ENDDO',
    'FOR': 'FOR',
    'FROM': 'FROM',
    'TO': 'TO',
    'DOWNTO': 'DOWNTO',
    'ENDFOR': 'ENDFOR',
    'READ': 'READ',
    'WRITE': 'WRITE'
}

tokens = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    'EQ',
    'NEQ',
    'LT',
    'GT',
    'LEQ',
    'GEQ',
    'LPAREN',
    'RPAREN',
    'SEMI',
    'ASSIGN',
    'num',
    'pidentifier',
    'COMMENTLINE',
    'COMMENTBRACKETS',
] + list(reserved.values())

reserved_re = '|'.join(reserved.values())

t_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_MODULO = r'\%'
t_EQ = r'\='
t_NEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_ASSIGN = r':='
t_pidentifier = r'[_a-z]+'
t_COMMENTLINE = r'\#(.*?(\\\n)*)+\n'
t_COMMENTBRACKETS = r'\[.*\]'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_num(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_CONTROL(t):
    r'[A-Z]+'
    controlToken = reserved.get(t.value)
    if(not controlToken):
        raise Exception("Bad control sequence '%s'" % t.value)
    t.type = controlToken
    return t

lexer = lex.lex()