import ply.lex as lex
import sys

words = 0

tokens = ('WORD', 'SPACES', 'STARTLINE', 'ENDLINE', 'NEWLINE')

def t_WORD(t):
    r'\w+'
    global words
    words += 1
    return t

def t_STARTLINE(t):
    r'^\s+'

def t_ENDLINE(t):
    r'\s+$'

def t_NEWLINE(t):
    r'\s*\n+\s*'
    # t.lexer.lineno += t.value.count('\n')
    t.lexer.lineno += 1
    t.value = '\n'
    return t

def t_SPACES(t):
    r'[\ \t]+'
    t.value = ' '
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
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
for tok in tokens:
    print(tok.value, end='')
print('\n\nlines:' + str(lexer.lineno))
print('words:' + str(words))