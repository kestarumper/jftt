import ply.lex as lex
import sys

def printError(str):
    print("\033[91m[Błąd]\033[0m: " + str)

class NotEnoughArguments(Exception):
    def __init__(self):
        Exception.__init__(self,"za mała liczba argumentów")

class NotEnoughOperators(Exception):
    def __init__(self):
        Exception.__init__(self,"za mała liczba operatorów")

class BadSymbol(Exception):
    def __init__(self, symbol):
        Exception.__init__(self,"zły symbol \"{}\"".format(symbol))

class InversePolishNotation:
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self, str):
        self.lexer.input(str)
        stack = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            if(tok.type == 'NUMBER'):
                stack.append(tok.value)
            else:
                try:
                    left = stack.pop()
                    right = stack.pop()
                    result = tok.action(right, left)
                    stack.append(result)
                except IndexError:
                    raise NotEnoughArguments
        if(len(stack) != 1):
            raise NotEnoughOperators
        return stack.pop()

    
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    'POWER',
)

# Tokens
def t_NUMBER(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("liczba %d jest za duża", t.value)
        t.value = 0
    return t

def t_PLUS(t):
    r'\+'
    t.action = lambda a,b : a + b
    return t

def t_MINUS(t):
    r'-'
    t.action = lambda a,b : a - b
    return t

def t_TIMES(t):
    r'\*'
    t.action = lambda a,b : a * b
    return t

def t_DIVIDE(t):
    r'\/'
    t.action = lambda a,b : a / b
    return t

def t_POWER(t):
    r'\^'
    t.action = lambda a,b : a ** b
    return t

def t_MODULO(t):
    r'%'
    t.action = lambda a,b : a % b
    return t




# Ignored characters
t_ignore = " \t"


def t_error(t):
    t.lexer.skip(1)
    raise BadSymbol(t.value[0])


# Build the lexer
lexer = lex.lex()
ipn = InversePolishNotation(lexer)

while True:
    toks = []
    try:
        s = input('ipn> ')   # Use raw_input on Python 2
        result = ipn.parse(s)
        print("= {}".format(result))
    except KeyboardInterrupt:
        print("\nBye")
        break
    except Exception as e:
        printError(str(e))
    
