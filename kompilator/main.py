from parser import parser, lexer
import sys


def prCyan(skk): print("\033[96m{}\033[00m".format(skk))


def prRed(skk): print("\033[91m{}\033[00m".format(skk))


def readFile(fname):
    with open(fname, "r") as file:
        return file.read()


def writeToFile(fname, data):
    with open(fname, "w") as file:
        file.write(data)


inputFile = sys.argv[1]
outFile = sys.argv[2]

try:
    data = readFile(inputFile)
    print("Compiling file '%s'" % inputFile)
    program = parser.parse(data, tracking=True)
    output = program.generateCode()
    writeToFile(outFile, output)
    print("Output file: '%s'" % outFile)
except SyntaxError as err:
    prRed(err)
