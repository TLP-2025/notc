from ply.lex import LexToken


class Expr: ...

class Assign(Expr):
     def __init__(self, name: LexToken, value:Expr):
          self.name = name
          self.value = value

class Binary(Expr):
        def __init__(self, leftExpr:Expr, operatorToken:LexToken, rightExpr: Expr):
            self.left = leftExpr
            self.operator = operatorToken
            self.right = rightExpr

class Unary(Expr):
    def __init__(self, operator: LexToken, expr: Expr):
        self.operator = operator
        self.expression = expr

class Literal(Expr):
    def __init__(self, value:any):
        self.value = value

class Grouping(Expr):
    def __init__(self, expr:Expr):
        self.expression = expr

class Identifier(Expr):
     def __init__(self, name: LexToken):
          self.name = name