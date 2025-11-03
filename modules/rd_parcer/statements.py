from ply.lex import LexToken
import modules.rd_parcer.expressions as Expr
from modules.lexer_rules import Token

class Stmt: ...

class Expression(Stmt):
    def __init__(self, expr: Expr.Expr):
        self.expression = expr

class Cout(Stmt):
    def __init__(self, exprs: list[Expr.Expr]):
        self.expressions: list[Expr.Expr] = exprs

# There should be a separate node for each type.
# But statements only need to be recognized, not evaluated
class Var(Stmt):
    def __init__(self, type:Token,  name:LexToken, initializer: Expr.Expr):
        self.type = type
        self.name = name
        self.initializer = initializer

class Block(Stmt):
    def __init__(self, stmts: list[Stmt]):
        self.statements = stmts