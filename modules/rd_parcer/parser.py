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
#                | forStmt 
#                | ifStmt 
#                | coutStmt 
#                | cinStmt 
#                | whileStmt 
#                | block;

# forStmt        → "for" "(" ( varDecl | exprStmt | ";" )
#                  expression? ";"
#                  expression? ")" statement ;

# whileStmt      → "while" "(" expression ")" statement ;

# ifStmt         → "if" "(" expression ")" statement
#                ( "else" statement )? ;

# block          → "{" declaration* "}" ;

# varsDecl        → ( "short" | "int" | "float" | "double" 
#                | "bool" | "char") (IDENTIFIER 
#                ( "=" expression )?)+ ";" ;

# exprStmt       → expression ";" ;
# coutStmt       → "cout" ("<<" expression)* ";" ;
# cinStmt        → "cin"  (">>" IDENTIFIER)* ";" ;

# -- EXPRESSIONS --
# expression     → assignment ;
# assignment     → IDENTIFIER "=" assignment
#                | logic_or ;

# logic_or       → logic_and ( "or" logic_and )* ;
# logic_and      → equality ( "and" equality )* ;

# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term           → factor ( ( "-" | "+" ) factor )* ;
# factor         → unary ( ( "/" | "*" | "%" ) unary )* ;
# unary          → ( "!" | "-" ) unary
#                | primary ;
# primary        → NUMBER | DECIMAL | STRING | "true" | "false" | ENDL
#                | "(" expression ")"
#                | IDENTIFIER ;

_variableTypes = [
    Token.BOOL,
    Token.CHAR,
    Token.DOUBLE,
    Token.FLOAT,
    Token.INT,
    Token.SHORT
]

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
            if (self.match(*_variableTypes)): return self.varsDeclaration()
            return self.statement()
        except ParseError as e:
            self._synchronize()
            return None
    

    def varsDeclaration(self) -> Stmt.Stmt:
        type = self.previous().type
        declarations: list[Stmt.Var] = []
        
        declarations.append(self._var_sub_declaration(type))
        
        while (self.match(Token.COMMA)):
            declarations.append(self._var_sub_declaration(type))
        
        self.consume(Token.SEMICOLON, "Expected ';' after variable declaration.")
        return Stmt.Vars(declarations)

    def _var_sub_declaration(self, type:LexToken) -> Stmt.Var:
        name: LexToken = self.consume(Token.IDENTIFIER, "Expected variable name.")
        initializer: Expr = None
        if (self.match(Token.EQUAL)):
            initializer = self.expression()
        
        return Stmt.Var(type, name, initializer)
    

    def statement(self) -> Stmt.Stmt:
        if (self.match(Token.FOR)): return self.forStatement()
        if (self.match(Token.IF)): return self.ifStatement()
        if (self.match(Token.COUT)): return self.coutStatement()
        if (self.match(Token.CIN)): return self.cinStatement()

        if (self.match(Token.WHILE)): return self.whileStatement()

        if (self.match(Token.LEFT_BRACE)): return self.block()

        return self.expressionStatement()

    def forStatement(self) -> Stmt.Stmt:
        self.consume(Token.LEFT_PAREN, "Expected '(' after 'for'.")

        initializer: Stmt.Stmt
        if (self.match(Token.SEMICOLON)):
            initializer = None
        elif (self.match(*_variableTypes)):
            initializer = self.varsDeclaration()
        else:
            initializer = self.expressionStatement()
        
        condition: Expr.Expr = None
        if (not self.check(Token.SEMICOLON)):
            condition = self.expression()
        self.consume(Token.SEMICOLON, "Expected ';' after loop condition.")

        increment: Expr.Expr = None
        if (not self.check(Token.RIGHT_PAREN)):
            increment = self.expression()
        self.consume(Token.RIGHT_PAREN, "Exptected ')' after for clauses")

        body = self.statement()

        # Desugaring

        ## execute increment at end of loop
        if (increment is not None):
            body = Stmt.Block([body, Stmt.Expression(increment)])
        
        if (condition is None):
            condition = Expr.Literal(True)
        body = Stmt.While(condition, body)

        if (initializer is not None):
            body = Stmt.Block([initializer, body])
        
        return body

    def whileStatement(self) -> Stmt.While:
        self.consume(Token.LEFT_PAREN, "Expected '(' after 'while'.")
        condition = self.expression()
        self.consume(Token.RIGHT_PAREN, "Expected '(' after condition.")

        body = self.statement()

        return Stmt.While(condition, body)

    
    def ifStatement(self) -> Stmt.If:
        self.consume(Token.LEFT_PAREN, "Expected '(' after 'if'.")
        condition = self.expression()
        self.consume(Token.RIGHT_PAREN, "Expected ')' after if condition.")

        thenBranch = self.statement()
        elseBranch = None
        if (self.match(Token.ELSE)):
            elseBranch = self.statement()
        
        return Stmt.If(condition, thenBranch, elseBranch)
        

    def coutStatement(self) -> Stmt.Cout:
        expressions:list[Expr.Expr] = []

        while(not self.match(Token.SEMICOLON)):
            self.consume(Token.LESS_LESS, "Expected '<<' after 'cout'.")
            expressions.append(self.expression())  
        return Stmt.Cout(expressions)
    
    def cinStatement(self) -> Stmt.Cin:
        vars:list[LexToken] = []

        while(not self.match(Token.SEMICOLON)):
            self.consume(Token.GREATER_GREATER, "Expected '>>' after 'cin'.")
            vars.append(self.consume(Token.IDENTIFIER, "Expected identifier after '>>'."))
        return Stmt.Cin(vars)
    

    def expressionStatement(self) -> Stmt.Expression:
        expr = self.expression()
        self.consume(Token.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def block(self) -> Stmt.Block:
        statements: list[Stmt.Stmt] = []

        while (not self.check(Token.RIGHT_BRACE) and not self.isAtEnd()):
            statements.append(self.declaration())
        
        self.consume(Token.RIGHT_BRACE, "Expected '}' after block.")
        return Stmt.Block(statements)



    ## Expressions

    def expression(self) -> Expr.Expr:
        return self.assignment()
    
    def assignment(self) -> Expr.Expr:
        expr = self.orExpr()

        if (self.match(Token.EQUAL)):
            equals = self.previous()
            value = self.assignment()

            if (isinstance(expr, Expr.Identifier)):
                name = expr.name
                return Expr.Assign(name, value)
            
            _error(equals, "Invalid assignment target.")

        return expr

    # binary operators
    def orExpr(self) -> Expr.Expr:
        expr = self.andExpr()

        while (self.match(Token.BAR_BAR)):
            operator = self.previous()
            right = self.andExpr()
            expr = Expr.Logical(expr, operator, right)
        
        return expr

    def andExpr(self) -> Expr.Expr:
        expr = self.equality()

        while (self.match(Token.AMP_AMP)):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)
        
        return expr
    
    def equality(self) -> Expr.Expr:
        expr = self.comparison()
        while (self.match(Token.BANG_EQUAL, Token.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def comparison(self) -> Expr.Expr:
        expr = self.term()

        while (self.match(Token.GREATER, Token.GREATER_EQUAL, Token.LESS, Token.LESS_EQUAL)):
            operator = self.previous()
            right: Expr = self.term()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def term(self) -> Expr.Expr:
        expr = self.factor()

        while (self.match(Token.MINUS, Token.PLUS)):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def factor(self) -> Expr.Expr:
        expr = self.unary()
        while (self.match(Token.SLASH, Token.STAR, Token.PERCENT)):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    # unary operators

    def unary(self) -> Expr.Expr:
        if (self.match(Token.BANG, Token.MINUS)):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        
        return self.primary()
    
    def primary(self) -> Expr.Expr:
        if (self.match(Token.FALSE)): return Expr.Literal(False)
        if (self.match(Token.TRUE)): return Expr.Literal(True)
        
        if (self.match(Token.NUMBER, Token.DECIMAL, Token.STRING, Token.ENDL)): return Expr.Literal(self.previous().value)

        if (self.match(Token.IDENTIFIER)):
            return Expr.Identifier(self.previous())
        
        if (self.match(Token.LEFT_PAREN)):
            expr = self.expression()
            self.consume(Token.RIGHT_PAREN, "Expected ')' after expression.")
            return Expr.Grouping(expr)
        
        print(f'DEBUG: {self.peek()}')

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
