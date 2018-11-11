import ply.lex as lex
import ply.yacc as yacc
import sys

words = 0

tokens = ('WORD', 'SPACE', 'STARTLINE', 'ENDLINE', 'NEWLINE')

def t_WORD(t):
    r'\w+'
    global words
    words += 1
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_STARTLINE(t):
    r'^[\ \t]+'
    return t

def t_ENDLINE(t):
    r'[\ \t]+$'
    return t

def t_SPACE(t):
    r'\ +'
    t.value = t.value[0]
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

data = '''          adrian
   rzeżucha           w majtach    
klucha             
'''

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
print(lexer.lineno)
print(words)