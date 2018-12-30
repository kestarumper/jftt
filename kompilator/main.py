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
    
fileNames = ['program0', 'program0a', 'program1']
for fname in fileNames:
    print("FILE: %s" % fname)
    data = readFile('examples/%s.imp' % fname)
    try:
        # lexer.input(data)
        # for tok in lexer:
        #     print(tok)
        program = parser.parse(data, tracking=True)
        output = program.generateCode()
        writeToFile('out/%s.mr' % fname, output)
        pass
    except SyntaxError as err:
        prRed(err)
        pass