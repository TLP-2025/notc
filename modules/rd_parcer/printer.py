import json
from modules.rd_parcer.expressions import *

def printTree(parseTree: Expr): print(toStr(parseTree))

def toStr(parseTree: Expr) -> str:
    match parseTree:    
        case Binary():
            return ' '.join([
                '(',
                parseTree.operator.value,
                toStr(parseTree.left),
                toStr(parseTree.right),
                ')'
            ])
        
        case Unary():
            return ' '.join(['(',
                  parseTree.operator.value,
                  toStr(parseTree.expression),
                  ')'
            ])
        case Grouping():
            return ' '.join(['(',
                  toStr(parseTree.expression),
                  ')'
            ])
        
        case Literal():
            return str(parseTree.value)