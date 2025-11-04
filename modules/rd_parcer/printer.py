import modules.rd_parcer.expressions as Expr
import modules.rd_parcer.statements as Stmt


def printStmts(statements: list[Stmt.Stmt]):
    for s in statements:
        print(stmtToStr(s))

def stmtToStr(statement:Stmt.Stmt, blocks:int = 0, blockSize = 4):
    offset = ' '*blocks*blockSize
    if (statement is None): return offset
    match statement:
        case Stmt.Cout():
            return offset + ' '.join([
                '(',
                'cout',
                ' '.join([toStr(e) for e in statement.expressions]),
                ')'
            ])
        

        case Stmt.Expression():
            return offset + ' '.join([
                '(',
                'EXPR',
                toStr(statement.expression),
                ')'
            ])
        
        case Stmt.Var():
            return offset + ' '.join([
                '(',
                f'[{statement.type}]',
                statement.name.value,
                toStr(statement.initializer),
                ')'
            ])
        
        case Stmt.Block():
            return offset + '{\n'+'\n'.join(
                [stmtToStr(s, blocks+1) for s in statement.statements]
            )+'\n'+offset+'}'
        
        case Stmt.If():
            return offset + f'\n'.join([
                '(',
                'if ' + toStr(statement.condition),
                stmtToStr(statement.thenBranch, blocks + 1),
                'else',
                stmtToStr(statement.elseBranch, blocks + 1),
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
        
        case Expr.Binary() | Expr.Logical():
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