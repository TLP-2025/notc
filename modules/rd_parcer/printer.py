import modules.rd_parcer.expressions as Expr
import modules.rd_parcer.statements as Stmt


def printStmts(statements: list[Stmt.Stmt]):
    for s in statements:
        print(stmtToStr(s, tabSize=0))

def stmtToStr(statement:Stmt.Stmt, tabSize = 4):
    offset = ' '*tabSize
    if (statement is None): return offset
    match statement:
        case Stmt.Cout():
            return offset + ' '.join([
                '(',
                'cout',
                ' '.join([toStr(e) for e in statement.expressions]),
                ')'
            ])
        
        case Stmt.Cin():
            return offset + ' '.join([
                '(',
                'cin',
                ' '.join([v.value for v in statement.variables]),
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

        case Stmt.Vars():
            return '\n'.join([offset + stmtToStr(s,0) for s in statement.declarations])
        
        case Stmt.Block():
            return '\n'.join(
                [f'{offset}{{']
                + [offset+stmtToStr(s) for s in statement.statements]
                + [f'{offset}}}']
            )
        
        case Stmt.If():
            return '\n'.join(map( lambda s: offset + s ,[
                '(if ' + toStr(statement.condition),
                stmtToStr(statement.thenBranch),
                'else',
                stmtToStr(statement.elseBranch),
                ')'
                
            ]))
        
        case Stmt.While():
            return '\n'.join(map(lambda s: offset+s, [
                f'(while {toStr(statement.condition)}',
                stmtToStr(statement.body),
                ')'
            ]))
    

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