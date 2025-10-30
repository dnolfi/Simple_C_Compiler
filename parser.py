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

        if self.tokenIndex >= len(self.tokens) - 1:
            return
        else :
            self.tokenIndex += 1
            return self.tokens[self.tokenIndex]["value"]
    
    def expect(self, expected) :
        actual = self.tokens[self.tokenIndex]['value']

        print("Expected:", expected, "Actual:", actual)
        if actual != expected :
            sys.stderr.write(
            f"\033[91m"
            f"Syntax error on line: {self.tokens[self.tokenIndex]['line']}"
            f"\nwhile processing token: {actual}"
            f"\ngot: {actual} but expected: {expected}"
            f"\033[0m\n"
            )
            exit(1)

        return self.advanceToken()
    
    # Expects: a constant OR operator (to be done later)
    # Returns: a Constant node
    def parseConst(self) :
        self.expect('2')
        return tr.Constant('2')

    # Expects: keyword, exp and semicol
    # Returns: a Statement node
    def parseStatement(self) :
        self.expect("return")
        return_val = self.parseConst()
        self.expect(";")

        statementNode = tr.Statement("return")
        statementNode.add_child(return_val)

        return statementNode


    # Expects: return type (void, int), identifier (main), open parenth, close parenth, obra and cbra
    # Returns: a function node
    def parseFunction(self) :
        # We need to expect a return type (int, void etc.)
        self.expect("int")
        # Expect a function identifier (main)
        self.expect("main")
        # Expect opening of function arguments
        self.expect("(")
        # Expect function arguments
        self.expect("void")
        # Expect closing of function args
        self.expect(")")
        # Expect opening of function body
        self.expect("{")

        # Now we can add the function node
        
        # Now we need to recursively descend into the function body
        statements = self.parseStatement()

        self.expect("}")

        functionNode = tr.Function("main")
        functionNode.add_child(statements)

        return functionNode

    # Keep parsing tokens to check for additional functions
    def parseProgram(self) :
        programNode = tr.Program()
        while(self.tokenIndex < len(self.tokens)) : 
            function = self.parseFunction()
            programNode.add_child(function)
        return programNode

# Need to load our dictionary of tokens from the lexer step
with open('tokens.json', 'r') as tokenFile :
    tokens = json.load(tokenFile)

# Used to index our list of token dictionaries
tokenListIndex = 0

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


