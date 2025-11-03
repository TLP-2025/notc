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
        
        case Stmt.Var():
            return ' '.join([
                '(',
                f'[{statement.type}]',
                statement.name.value,
                toStr(statement.initializer),
                ')'
            ])
        
    

def toStr(parseTree: Expr.Expr) -> str:
    if (parseTree is None): return ''
    match parseTree:   
        case Expr.Assign():
            return ' '.join([
                '(',
                parseTree.name.value,
                '=',
                toStr(parseTree.value),
                ')'
            ])
        
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
        
        case Expr.Identifier():
            return str(parseTree.name.value)