from enum import Enum

class Token(Enum):
    # Single-character tokens.
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'

    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    PERCENT = 'PERCENT'
    SEMICOLON = 'SEMICOLON'
    SLASH = 'SLASH'
    STAR = 'STAR'


    # One or two character tokens.
    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'

    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'

    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'

    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'

    AMP_AMP = 'AMP_AMP'
    BAR_BAR = 'BAR_BAR'

    LESS_LESS = 'LESS_LESS'
    GREATER_GREATER = 'GREATER_GREATER'


    # Literals.
    CHAR_LITERAL = 'CHAR_LITERAL'
    DECIMAL = 'DECIMAL'
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'


    # Keywords.
    AND = 'AND'
    BOOL = 'BOOL'
    CHAR = 'CHAR'
    CIN = 'CIN'
    COUT = 'COUT'
    DOUBLE = 'DOUBLE'
    ELSE = 'ELSE'
    ENDL = 'ENDL'
    FALSE = 'FALSE'
    FLOAT = 'FLOAT'
    FOR = 'FOR'
    IF = 'IF'
    INT = 'INT'
    OR = 'OR'
    SHORT = 'SHORT'

    TRUE = 'TRUE'
    WHILE = 'WHILE'

# Mapping for lex library
tokens = tuple(map(lambda name: Token[name].value, Token._member_names_,))


# Regular expression rules
## Single-character tokens.
t_LEFT_PAREN = r'\('
t_RIGHT_PAREN = r'\)'
t_LEFT_BRACE = r'{'
t_RIGHT_BRACE = r'}'

t_COMMA = r','
t_DOT = r'\.'
t_MINUS = r'-'
t_PLUS = r'\+'
t_SEMICOLON = r';'
#SLASH defined after comments
t_STAR = r'\*'
t_PERCENT = r'\%'


## One or two character tokens.
t_BANG = r'!'
t_BANG_EQUAL = r'!='
t_EQUAL = r'='
t_EQUAL_EQUAL = r'=='
t_GREATER = r'>'
t_GREATER_EQUAL = r'>='
t_LESS = r'<'
t_LESS_EQUAL = r'<='

t_LESS_LESS = r'<<'
t_GREATER_GREATER = r'>>'

t_AMP_AMP = r'&&'
t_BAR_BAR = r'\|\|'


# Keywords.
def t_BOOL(t):
    r'bool'
    return t
def t_CHAR(t):
    r'char'
    return t
def t_CIN(t):
    r'CIN'
    return t
def t_COUT(t):
    r'COUT'
    return t
def t_DOUBLE(t):
    r'double'
    return t
def t_ELSE(t):
    r'else'
    return t
def t_ENDL(t):
    r'endl'
    return t
def t_FALSE(t):
    r'false'
    return t
def t_FLOAT(t):
    r'float'
    return t
def t_FOR(t):
    r'for'
    return t
def t_IF(t):
    r'if'
    return t
def t_INT(t):
    r'int'
    return t
def t_SHORT(t):
    r'short'
    return t
def t_TRUE(t):
    r'true'
    return t
def t_WHILE(t):
    r'while'
    return t


## Literals.
t_CHAR_LITERAL = r'\'\w\''
def t_IDENTIFIER(t): r'[_a-zA-Z]+(?:_|\w)*'; return t
t_STRING = r'\".*\"'
def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t



# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ignore_comment(t):
    r'//.*'
    t.lexer.lineno += len(t.value)

def t_SLASH(t):
    r'/'
    return t
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def onCharError(char, line): ...

# Error handling rule
def t_error(t):
    onCharError(t.value[0], t.lexer.lineno)
    t.lexer.skip(1)
