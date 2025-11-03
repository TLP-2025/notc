from ply.lex import LexToken
from modules.lexer_rules import Token

hadError = False


def error(line: int, msg: str):
    report(line, "", msg)


def parseError(token: LexToken, msg: str):
    if (token.type == Token.EOF):
        report(token.lineno, " at end", msg)
    else:
        report(token.lineno, f" at '{token.value}'", msg)



def report(line:int, location:str, msg:str):
    global hadError 
    hadError = True
    print(f"[line {line}] Error {location}: {msg}")
