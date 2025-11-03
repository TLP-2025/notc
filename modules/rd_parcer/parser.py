from modules.lexer_rules import Token
from ply.lex import LexToken
from modules import state
from modules.rd_parcer.expressions import *

# GRAMMAR
# expression     → equality ;
# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term           → factor ( ( "-" | "+" ) factor )* ;
# factor         → unary ( ( "/" | "*" ) unary )* ;
# unary          → ( "!" | "-" ) unary
#                | primary ;
# primary        → NUMBER | STRING | "true" | "false" | "nil"
#                | "(" expression ")" ;


class RDParser:
    def __init__(self,tokens:list[LexToken]):
        self.tokens: list[LexToken] = tokens
        self.current: int = 0

    
    def parse(self) -> Expr:
        try:
            return self.expression()
        except ParseError as er:
            return None

    # RD methods

    def expression(self) -> Expr:
        return self.equality()

    # binary operators
    def equality(self) -> Expr:
        expr = self.comparison()
        while (self.match(Token.BANG_EQUAL, Token.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def comparison(self) -> Expr:
        expr:Expr = self.term()

        while (self.match(Token.GREATER, Token.GREATER_EQUAL, Token.LESS, Token.LESS_EQUAL)):
            operator = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def term(self) -> Expr:
        expr: Expr = self.factor()

        while (self.match(Token.MINUS, Token.PLUS)):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def factor(self) -> Expr:
        expr: Expr = self.unary()
        while (self.match(Token.SLASH, Token.STAR)):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr
    
    # unary operators

    def unary(self) -> Expr:
        if (self.match(Token.BANG, Token.MINUS)):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self) -> Expr:
        if (self.match(Token.FALSE)): return Literal(False)
        if (self.match(Token.TRUE)): return Literal(True)
        
        if (self.match(Token.NUMBER, Token.DECIMAL, Token.STRING)): return Literal(self.previous().value)

        if (self.match(Token.LEFT_PAREN)):
            expr = self.expression()
            self.consume(Token.RIGHT_PAREN)
            return Grouping(expr)

        raise _error(self.peek(), "Expected expresion.")
        
        
    



            




    # Base methods
        
        
    def consume(self, type: Token):
        if (self.check(type)): return self.advance()

        raise _error(self.peek(), f"Expected {type.value} after expression")

    def match(self, *tokenTypes: Token) -> bool:
        for t in tokenTypes:
            if (self.check(t)):
                self.advance()
                return True
            
        return False
    

    def check(self, tokenType: Token) -> bool: 
        if (self.isAtEnd()): return False
        return self.peek().type == tokenType.value
    
    def advance(self) -> LexToken:
        if (not self.isAtEnd()): self.current+=1
        return self.previous()
    
    def isAtEnd(self) -> bool:
        return self.peek().type == Token.EOF
    
    def peek(self) -> LexToken:
        return self.tokens[self.current]

    def previous(self) -> LexToken:
        return self.tokens[self.current-1]
    
    
    ## Error handling
    # Drop tokens until after ';' or beggining of statement
    def _synchronize(self):
        self.advance()

        while(not self.isAtEnd()):
            if (self.previous().type == Token.SEMICOLON): return

            match self.peek().type:
                case Token.BOOL |Token.CHAR |Token.CIN |Token.COUT |Token.DOUBLE |Token.ELSE |Token.ENDL |Token.FALSE |Token.FLOAT |Token.FOR |Token.IF |Token.INT |Token.SHORT |Token.TRUE |Token.WHILE:
                    return
                
            self.advance()

                
## Error class to stop parsing
class ParseError(RuntimeError): ...

def _error(token: LexToken, message: str) -> ParseError:
    state.parseError(token, message)
    return ParseError()
