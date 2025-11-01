import ply.lex as _lex
from modules import lexer_rules as _rules
from modules import state

_rules.onCharError = lambda char, line: state.reportError(__name__, f"Illegal character '{char}' in line {line}")
_lexer = _lex.lex(module=_rules)

def tokens(source):
    _lexer.input(source)
    
    while True:
        token = _lex.token()
        if (not token): break
        yield token

