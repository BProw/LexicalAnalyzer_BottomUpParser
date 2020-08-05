from enum import IntEnum
import sys

# all char classes
class CharClass(IntEnum):
    EOF        = 0
    LETTER     = 1
    DIGIT      = 2
    OPERATOR   = 3
    PUNCTUATOR = 4
    QUOTE      = 5
    BLANK      = 6
    DELIMITER  = 7
    COMPARISON = 8              # Added for <, >, >=, <= (3.3.20)
    OTHER      = 9

# Tokens from specs.
class Token(IntEnum):
    EOF             = 0
    INT_TYPE        = 1
    MAIN            = 2
    OPEN_PAR        = 3
    CLOSE_PAR       = 4
    OPEN_CURLY      = 5
    CLOSE_CURLY     = 6
    OPEN_BRACKET    = 7
    CLOSE_BRACKET   = 8
    COMMA           = 9
    ASSIGNMENT      = 10
    SEMICOLON       = 11
    IF              = 12
    ELSE            = 13
    WHILE           = 14
    OR              = 15
    AND             = 16
    EQUALITY        = 17
    INEQUALITY      = 18
    LESS            = 19
    LESS_EQUAL      = 20
    GREATER         = 21
    GREATER_EQUAL   = 22
    ADD             = 23
    SUBTRACT        = 24
    MULTIPLY        = 25
    DIVIDE          = 26
    BOOL_TYPE       = 27
    FLOAT_TYPE      = 28
    CHAR_TYPE       = 29
    IDENTIFIER      = 30
    INT_LITERAL     = 31
    TRUE            = 32
    FALSE           = 33
    FLOAT_LITERAL   = 34
    CHAR_LITERAL    = 35

# Lexeme lookup for types
lookupTypes = {
    "int"       : Token.INT_TYPE,
    "bool"      : Token.BOOL_TYPE,
    "float"     : Token.FLOAT_TYPE,
    "char"      : Token.CHAR_TYPE
}

# Lookup for control .
lookupConstructs = {
    "if"        : Token.IF,
    "else"      : Token.ELSE,
    "while"     : Token.WHILE
}

# lexeme to token conversion map
lookup = {
    "main"      : Token.MAIN,

    ";"         : Token.SEMICOLON,
    "*"         : Token.MULTIPLY,
    "/"         : Token.DIVIDE,
    "+"         : Token.ADD,
    "-"         : Token.SUBTRACT,

    "if"        : Token.IF,
    "else"      : Token.ELSE,
    "while"     : Token.WHILE,

    "&&"        : Token.AND,
    "||"        : Token.OR,
    "="         : Token.ASSIGNMENT,

    "<"         : Token.LESS,
    ">"         : Token.GREATER,
    "<="        : Token.LESS_EQUAL,
    ">="        : Token.GREATER_EQUAL,
    "=="        : Token.EQUALITY,          
    "!="        : Token.INEQUALITY,         
    ","         : Token.COMMA,

    "true"      : Token.TRUE,               
    "false"     : Token.FALSE,             

    "("         : Token.OPEN_PAR,
    ")"         : Token.CLOSE_PAR,
    "{"         : Token.OPEN_CURLY,
    "}"         : Token.CLOSE_CURLY,
    "["         : Token.OPEN_BRACKET,
    "]"         : Token.CLOSE_BRACKET
 }

# Error code to message conversion function                
def errorMessage(code):
    msg = "Error " + str(code).zfill(2) + ": "
    if code == 3:
        return msg + "Lexical error."
    return msg + " syntax error."

def wut(token):
    print(token)

# reads the next char from input and returns its class
def getChar(input):
    if len(input) == 0:
        return (None, CharClass.EOF)
    c = input[0].lower()
    if c.isalpha():
        return (c, CharClass.LETTER)
    if c.isdigit():
        return (c, CharClass.DIGIT)
    if c == '\'':                   # <----- ADDED SINGLE QUOTE (3.3.20)
        return (c, CharClass.QUOTE)
    if c in ['+', '-', '*', '/', '.', '!']:
        return (c, CharClass.OPERATOR)
    if c in [',', ';']:              
        return(c, CharClass.PUNCTUATOR)
    if c in [' ', '\n', '\t']:
        return(c, CharClass.BLANK)
    if c in ['=','<', '>', '<=', '>=', '&', '|', '==', '!=']:
        return(c, CharClass.COMPARISON)
    if c in ['(', ')', '{', '}', '[', ']']:
        return(c, CharClass.DELIMITER)
    return(c, CharClass.OTHER)

# calls getChar and addChar until it returns a non-blank
def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

# returns the next (lexeme, token) pair or ("", EOF) if EOF is reached
def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # checks EOF
    if charClass == CharClass.EOF:
        return(input, lexeme, Token.EOF)

    # Read letter, find match in one of the lookups.
    if charClass == CharClass.LETTER:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.LETTER or charClass == charClass.DIGIT:
                input, lexeme = addChar(input, lexeme)
            else:
                if lexeme in lookup:
                    return(input, lexeme, lookup[lexeme])           # Keyword
                if lexeme in lookupTypes:
                    return(input, lexeme, lookupTypes[lexeme])      # Literal
                if lexeme in lookupConstructs:
                    return(input, lexeme, lookupConstructs[lexeme])   # Control statements.
                return(input, lexeme, Token.IDENTIFIER)             # Identifier 
   
    # TODOd (3.3.20)
    if charClass == CharClass.DIGIT:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.DIGIT or charClass == CharClass.OPERATOR: 
                input, lexeme = addChar(input, lexeme)
            else:
                if '.' in lexeme:                              # '.' means float value found.
                    return(input, lexeme, Token.FLOAT_LITERAL)
                return(input, lexeme, Token.INT_LITERAL)       # No '.' = int literal.
 
    # reads operator
    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookup:
            return(input, lexeme, lookup[lexeme])

    # Read punctuator.
    if charClass == CharClass.PUNCTUATOR:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookup:
            return(input, lexeme, lookup[lexeme])

    # Read single quote for CHAR_LITERAL.
    if charClass == CharClass.QUOTE:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == charClass.LETTER or charClass == CharClass.QUOTE:
                input, lexeme = addChar(input, lexeme) 
            else:
                return(input, lexeme, Token.CHAR_LITERAL)

    # Read comparison or in/equality operators. 
    if charClass == CharClass.COMPARISON or charClass == CharClass.OPERATOR:
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.COMPARISON:  
                input, lexeme = addChar(input, lexeme)
            else:
                if lexeme in lookup: 
                    return(input, lexeme, lookup[lexeme])  
        return(input, lexeme, lookup[lexeme])               
    

    # reads parenthesis, braces, and curly brackets. 
    if charClass == CharClass.DELIMITER:
        input, lexeme = addChar(input, lexeme)
        return(input, lexeme, lookup[lexeme])

    # anything else, raises Lexical Error 
    raise Exception(errorMessage(3))
# main
if __name__ == "__main__":

    # checks if source file was passed and if it exists
    try:
        if len(sys.argv) != 2:
            raise ValueError(errorMessage(1))
        sourceFile = None
        try:
            sourceFile = open(sys.argv[1], "rt")
        except:
            pass
        if not sourceFile:
            raise IOError(errorMessage(2))
        input = sourceFile.read()
        sourceFile.close()
    except Exception as ex:
        print(ex)
        sys.exit(1)

    # main loop
    output = []
    while True:
        input, lexeme, token = lex(input)
        if token == Token.EOF:
            break
        output.append((lexeme, token))

    # # prints the output
    for (lexeme, token) in output:
        print(lexeme, token)