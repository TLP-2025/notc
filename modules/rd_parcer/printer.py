import modules.rd_parcer.expressions as Expr
import modules.rd_parcer.statements as Stmt


def printStmts(statements: list[Stmt.Stmt]):
    for s in statements:
        print(stmtToStr(s))

def stmtToStr(statement:Stmt.Stmt):
    match statement:
        case Stmt.Cout():
            return ' '.join([
                '(',
                'cout',
                ' '.join([toStr(e) for e in statement.expressions]),
                ')'
            ])
        

        case Stmt.Expression():
            return ' '.join([
                '(',
                'EXPR',
                toStr(statement.expression),
                ')'
            ])
    

def toStr(parseTree: Expr.Expr) -> str:
    match parseTree:    
        case Expr.Binary():
            return ' '.join([
                '(',
                parseTree.operator.value,
                toStr(parseTree.left),
                toStr(parseTree.right),
                ')'
            ])
        
        case Expr.Unary():
            return ' '.join(['(',
                  parseTree.operator.value,
                  toStr(parseTree.expression),
                  ')'
            ])
        case Expr.Grouping():
            return ' '.join(['(',
                  toStr(parseTree.expression),
                  ')'
            ])
        
        case Expr.Literal():
            return str(parseTree.value)