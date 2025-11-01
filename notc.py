import sys
from modules import parcer

def test(source):
    parcer.test(source)


def runPrompt():
    while (True):
        try:
            line = input("notc> ")
            if (line == ""): continue
        except EOFError: break
        except KeyboardInterrupt: break
        test(line)

def runFile(path):
    with open(path) as file:
        test(file.read())

match len(sys.argv)-1:
    case 0:
        runPrompt()
    case 1:
        path = sys.argv[1]
        runFile(path)
    case _:
        sys.exit(64)
        

