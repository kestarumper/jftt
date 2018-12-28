from tokenizer import lexer
# from parser import parser

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

lexer.input(data)
for tok in lexer:
    print(tok)

# result = parser.parse(data)
# print(result)
# writeToFile('program.imp.copy', result)