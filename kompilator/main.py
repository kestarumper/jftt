from parser import parser, lexer

def prCyan(skk): print("\033[96m{}\033[00m".format(skk))
def prRed(skk): print("\033[91m{}\033[00m".format(skk))

def readFile(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            data.append(line)
    return ''.join(data)

def writeToFile(fname, lines):
    with open(fname, "w") as file:
        for line in lines:
            file.write(line + '\n')
    
data = readFile('program.imp')


try:
    lexer.input(data)
    for tok in lexer:
        print(tok)
    result = parser.parse(data, tracking=True)
    print(result)
    writeToFile('program.imp.copy', result)
    pass
except SyntaxError as err:
    prRed(err)
    pass