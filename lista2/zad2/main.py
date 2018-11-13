import ply.lex as lex
import sys

tokens = ['COMMENT', 'NEWLINE', 'HTMLTAG', 'TEXT']
MODE_IN_SCRIPT = False

def t_SCRIPTOPEN(t):
    r'<script>'
    global MODE_IN_SCRIPT
    MODE_IN_SCRIPT = True
    print(t.value, end='')

def t_SCRIPTCLOSE(t):
    r'</script>'
    global MODE_IN_SCRIPT
    MODE_IN_SCRIPT = False
    print(t.value, end='')

def t_JSCOMMENT(t):
    r'\/\/.*\n'
    global MODE_IN_SCRIPT
    if not MODE_IN_SCRIPT:
        print(t.value)

def t_COMMENT(t):
    r'<!--(.|\n|\/)*?-->\n*'
    print("\033[93m", file=sys.stderr, end='')
    print(t, file=sys.stderr)
    print("\033[0m", file=sys.stderr, end='')
    # return t

def t_NEWLINE(t):
    r'\n+'
    print(t.value, end='')

def t_HTMLTAG(t):
    r'</?[a-zA-Z]+\s*.*/?>'
    print(t.value, end='')
# t_TEXT = r'=|\"|\'|.+'

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
for tok in tokens:
    print(tok.value, end='')