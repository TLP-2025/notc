import sys
from modules import scanner
from modules.rd_parcer.parser import RDParser
from modules.rd_parcer.printer import printTree
from modules import state


def run(source:str):
    tokens = list(scanner.tokens(source))
    # print(tokens)
    parser = RDParser(tokens)

    result = parser.parse()

    if (state.hadError): return
    printTree(result)
    print ("Accepted")


def runPrompt():
    while (True):
        try:
            line = input("notc> ")
            if (line == ""): continue
        except EOFError: break
        except KeyboardInterrupt: break
        run(line)
        state.hadError = False

def runFile(path):
    with open(path) as file:
        run(file.read())

match len(sys.argv)-1:
    case 0:
        runPrompt()
    case 1:
        path = sys.argv[1]
        runFile(path)
    case _:
        sys.exit(64)
        

