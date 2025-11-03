from modules.lexer_rules import Token
from ply.lex import LexToken
from modules import state
import modules.rd_parcer.expressions as Expr
import modules.rd_parcer.statements as Stmt


# GRAMMAR
# -- STATEMENTS --
# program        → declaration* EOF ;

# declaration    → varDecl
#                | statement ;

# statement      → exprStmt
#                | coutStmt ;

# varDecl        → ( "short" | "int" | "float" | "double" 
#                | "bool" | "char") IDENTIFIER 
#                ( "=" expression )? ";" ;

# exprStmt       → expression ";" ;
# coutStmt       → "cout" expression ";" ;

# -- EXPRESSIONS --
# expression     → equality ;
# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term           → factor ( ( "-" | "+" ) factor )* ;
# factor         → unary ( ( "/" | "*" ) unary )* ;
# unary          → ( "!" | "-" ) unary
#                | primary ;
# primary        → NUMBER | DECIMAL | STRING | "true" | "false"
#                | "(" expression ")"
#                | IDENTIFIER ;


class RDParser:
    def __init__(self,tokens:list[LexToken]):
        self.tokens: list[LexToken] = tokens
        self.current: int = 0

    
    def parse(self) -> list[Stmt.Stmt]:
        statements: list[Stmt.Stmt] = []

        while (not self.isAtEnd()):
            statements.append(self.declaration())
        
        return statements

    # RD methods

    def declaration(self) -> Stmt.Stmt:
        try:
            if (self.match(Token.SHORT, Token.INT, Token.FLOAT, Token.DOUBLE, Token.CHAR, Token.BOOL)): return self.varDeclaration()
            return self.statement()
        except ParseError as e:
            self._synchronize()
            return None
    
    # multi variable declaration not allowed
    # would need a varsDeclaration rule containing multiple varDeclaration
    def varDeclaration(self) -> Stmt.Stmt:
        type = self.previous().type
        name: LexToken = self.consume(Token.IDENTIFIER, "Expected variable name.")

        initializer: Expr = None
        if (self.match(Token.EQUAL)):
            initializer = self.expression()
        
        self.consume(Token.SEMICOLON, "Expected ';' after variable declaration.")
        return Stmt.Var(type, name, initializer)

    def statement(self) -> Stmt.Stmt:
        if (self.match(Token.COUT)): return self.coutStatement()
        # if (self.match(Token.CIN)): return self.cinStatement()

        return self.expressionStatement()
    
    def coutStatement(self):
        expressions:list[Expr.Expr] = []

        while(not self.match(Token.SEMICOLON)):
            self.consume(Token.LESS_LESS, "Expected '<<' after 'cout'.")
            expressions.append(self.expression())  
        return Stmt.Cout(expressions)
    

    def expressionStatement(self):
        expr = self.expression()
        self.consume(Token.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)




    ## Expressions

    def expression(self) -> Expr:
        return self.equality()

    # binary operators
    def equality(self) -> Expr:
        expr = self.comparison()
        while (self.match(Token.BANG_EQUAL, Token.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def comparison(self) -> Expr:
        expr:Expr = self.term()

        while (self.match(Token.GREATER, Token.GREATER_EQUAL, Token.LESS, Token.LESS_EQUAL)):
            operator = self.previous()
            right: Expr = self.term()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def term(self) -> Expr:
        expr: Expr = self.factor()

        while (self.match(Token.MINUS, Token.PLUS)):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def factor(self) -> Expr:
        expr: Expr = self.unary()
        while (self.match(Token.SLASH, Token.STAR)):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    # unary operators

    def unary(self) -> Expr:
        if (self.match(Token.BANG, Token.MINUS)):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        
        return self.primary()
    
    def primary(self) -> Expr:
        if (self.match(Token.FALSE)): return Expr.Literal(False)
        if (self.match(Token.TRUE)): return Expr.Literal(True)
        
        if (self.match(Token.NUMBER, Token.DECIMAL, Token.STRING)): return Expr.Literal(self.previous().value)

        if (self.match(Token.IDENTIFIER)):
            return Expr.Identifier(self.previous())
        
        if (self.match(Token.LEFT_PAREN)):
            expr = self.expression()
            self.consume(Token.RIGHT_PAREN, "Expected ')' after expression.")
            return Expr.Grouping(expr)

        raise _error(self.peek(), "Expected expression.")
        
        
    



            




    # Base methods
        
        
    def consume(self, type: Token, msg:str):
        if (self.check(type)): return self.advance()

        raise _error(self.peek(), msg)

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
