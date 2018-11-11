import ply.lex as lex
import sys

tokens = ['COMMENT', 'NEWLINE', 'HTMLTAG', 'INNERHTML']

t_NEWLINE = r'\n+'
t_HTMLTAG = r'</?[a-zA-Z]+\s*.*/?>'
t_INNERHTML = r'\"|\'|.+'

def t_COMMENT(t):
    r'<!--(.|\n|\/)*?-->\n*'
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