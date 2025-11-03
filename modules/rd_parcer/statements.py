from ply.lex import LexToken
import modules.rd_parcer.expressions as Expr

class Stmt: ...

class Expression(Stmt):
    def __init__(self, expr: Expr.Expr):
        self.expression = expr

class Cout(Stmt):
    def __init__(self, exprs: list[Expr.Expr]):
        self.expressions: list[Expr.Expr] = exprs