import ply.lex as lex
import sys

tokens = ['LINECOMMENT', 'DOCCOMMENT', 'BLOCKCOMMENT']

def t_STRING(t):
    r'(\".*?\")|(\'.*?\')'
    print(t.value, end='')

def t_LINECOMMENT(t):
    r'(\/\/.*\n)'
    print(t, file=sys.stderr)

def t_DOCCOMMENT(t):
    r'(\/\*{2}(.|\n)*?\*\/)'
    print(t, file=sys.stderr)

def t_BLOCKCOMMENT(t):
    r'(\/\*(.|\n)*?\*\/)'
    print(t, file=sys.stderr)

def t_error(t):
    print(t.value[0], end='')
    t.lexer.skip(1)

lexer = lex.lex()

lines = [line for line in sys.stdin]
data = ''.join(lines)

lexer.input(data)
tokens = []

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok, file=sys.stderr)
    tokens.append(tok)