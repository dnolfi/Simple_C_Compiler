# The parser will accept the list of tokens produced by the lexer and generate a tree representation
# called an abstract syntax tree

# Define abstract class for each type of node, define classes that extend the type of node.
# Ex: Define Exp abstract class, and Constant and BinaryExp classes that extend it
# First step is to construct an abstract syntax tree
import tree as tr
import json
import sys
import pprint as pp

class Parser :
    # Constructor
    def __init__(self, tokens) :
        self.tokens = tokens
        self.tokenIndex = 0

    # Need to write a few helper functions based on the grammar rules to successfully parse the tokens from the lexer
    # Functions should be: parseFunction(), parseStatement(), parseConstant()
    # Helper functions should be expect() and advanceTokens()
    def advanceToken(self) :
        self.tokenIndex += 1
        
    def syntaxError(self, expected, actual) :
        if self.tokenIndex >= len(self.tokens) :
            lineInfo = "EOF"
        else :
            lineInfo = self.tokens[self.tokenIndex]['line']

        sys.stderr.write(
        f"\033[91m"
        f"Syntax error on line: {lineInfo}"
        f"\nwhile processing token: {actual}"
        f"\ngot: {actual} but expected: {expected}"
        f"\033[0m\n"
        )            
        exit(1)
    
    def expect(self, expected) :
        if self.tokenIndex >= len(self.tokens) :
            self.syntaxError(expected, "EOF")
        # We want to check the type of the token, and then check if it is correct
        else :
            actual = self.tokens[self.tokenIndex]

        print("Expected:", expected, "Actual:", actual)
        if actual['type'] != expected :
            self.syntaxError(expected, actual)

        self.advanceToken()
        return actual
    
    # Expects: a constant OR operator (to be done later)
    # Returns: a Constant node
    def parseConst(self) :
        constVal = self.expect('const')
        return tr.Constant(constVal['value'])

    # Expects: keyword, exp and semicol
    # Returns: a Statement node
    def parseStatement(self) :
        ret = self.expect('kw')
        return_val = self.parseConst()
        self.expect('semcol')

        statementNode = tr.Statement(ret['value'])
        statementNode.add_child(return_val)

        return statementNode


    # Expects: return type (void, int), identifier (main), open parenth, close parenth, obra and cbra
    # Returns: a function node
    def parseFunction(self) :
        # We need to expect a return type (int, void etc.)
        # Thus we need to expect int or void for now
        funcRtrnType = self.expect('kw')
        if funcRtrnType['value'] not in ('int', 'void') :
            self.syntaxError(funcRtrnType, 'kw')

        # Expect a function identifier (main)
        funcName = self.expect('id')
        # Expect opening of function arguments
        self.expect('opar')
        # Expect function arguments
        paramType = self.expect('kw')
        if paramType['value'] != "void" :
            self.syntaxError("void", paramType['value']) 
        # Expect closing of function args
        self.expect('cpar')
        # Expect opening of function body
        self.expect('obra')
        
        # Now we need to recursively descend into the function body
        statements = self.parseStatement()

        self.expect('cbra')

        # Now we can add the function node
        functionNode = tr.Function(funcRtrnType['value'], funcName['value'])
        functionNode.add_child(statements)

        return functionNode

    # Keep parsing tokens to check for additional functions
    def parseProgram(self) :

        programNode = tr.Program()
        while(self.tokenIndex < len(self.tokens)) : 
            # Peek at the next token
            current = self.tokens[self.tokenIndex]
            # Check if the next token has a return type

            if current['type'] == 'kw' and current['value'] in ('int', 'void'):
                func = self.parseFunction()
                programNode.add_child(func)
            
            else:

                # If not, program is over or we found an error
                self.syntaxError('return type', current['type'])
        return programNode

# Need to load our dictionary of tokens from the lexer step
with open('tokens.json', 'r') as tokenFile :
    tokens = json.load(tokenFile)


# Want to define a set of grammar rules so that we know how to classify our tokens in the tree. Ex:

# <program> ::= <function>
# <function> ::= "int" <identifier> "(" "void" ")" "{" <statement> "}"
# <statement> ::= "return" <exp> ";"
# <exp> ::= <int>
# <identifier> ::= ? An identifier token ?
# <int> ::= ? A constant token ?

# Using the grammar rules, we can create our tree and then move on to generating assembly to create the
# actual executable program

# It's called recursive descent parsing because the parsing functions recursively call eachother to verify the next token
# Ex: We call parseFunction(), which verifies that the function was defined properly
#     parseFunction() then calls parseStatement(), which in turn calls parseConstant(), and the process repeats until 
#     parseFunction() returns the node

# Should take the tokens provvided in 'lexer.py' and then create a corresponding node for each token
# The list of possible tokens we have is:
# id, kw, obra, cbra, opar, cpar, const, semcol

# Root node of the AST is our program node

parser = Parser(tokens)

tree = parser.parseProgram()

tree.pretty_print()

tokenFile.close()


