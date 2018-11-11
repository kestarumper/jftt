import ply.lex as lex
import sys

tokens = ['COMMENT', 'NEWLINE', 'HTMLTAG', 'TEXT']

t_NEWLINE = r'\n+'
t_HTMLTAG = r'</?[a-zA-Z]+\s*.*/?>'
t_TEXT = r'\"|\'|.+'

def t_COMMENT(t):
    r'<!--(.|\n|\/)*?-->\n*'
    print("\033[93m", file=sys.stderr, end='')
    print(t, file=sys.stderr)
    print("\033[0m", file=sys.stderr, end='')
    # return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0], file=sys.stderr)
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