import sys  # This is to read the cmd line args
import re
import json

if  len(sys.argv) < 2 :
    print("Lexer Error: Must provide source file in command line arguments.")
    exit(1)

print("File to read is: ", sys.argv[1]) # Just for debugging

if not sys.argv[1].endswith('.c') :
    print("Lexer Error: Input must be a .c file for compilation. Compilation aborted.")
    exit(1)

# Open the source file we passed as our argument, after checking to make sure the file is a .c file!
source_file = open(sys.argv[1])
source_code = source_file.read()

# Using the following table for our tokens and their regular expressions
identifier = re.compile(r"[a-zA-Z_]\w*\b")
constant = re.compile(r"[0-9]+\b") 
keyword = re.compile(r"\b(int|void|return)\b")
open_parenth = re.compile(r"\(")
close_parenth = re.compile(r"\)")
open_brace = re.compile(r"{")
close_brace = re.compile(r"}")
semi_col = re.compile(r";")

found_tokens = []

def checkToken(token, lineNum) :
    if identifier.fullmatch(token) :
        if keyword.fullmatch(token) :
            print("KEYWORD:", token, "on line:", lineNum)
            found_tokens.append(("KEYWORD", token, lineNum))
        else :
            print("IDENTIFIER:", token, "on line:", lineNum)
            found_tokens.append(("IDENTIFIER", token, lineNum))
    elif constant.fullmatch(token) :
        print("CONSTANT:", token, "on line:", lineNum)
        found_tokens.append(("CONSTANT", token, lineNum))
    elif open_parenth.fullmatch(token) :
        print("OPEN PARENTHESIS:", token, "on line:", lineNum)
        found_tokens.append(("OPEN PARENTHESIS", token, lineNum))
    elif close_parenth.fullmatch(token) :
        print("CLOSE PARENTHESIS:", token, "on line:", lineNum)
        found_tokens.append(("CLOSE PARENTHESIS", token, lineNum))
    elif open_brace.fullmatch(token) :
        print("OPEN BRACE:", token, "on line:", lineNum)
        found_tokens.append(("OPEN BRACE", token, lineNum))
    elif close_brace.fullmatch(token) :
        print("CLOSE BRACE:", token, "on line:", lineNum)
        found_tokens.append(("CLOSE BRACE", token, lineNum))
    elif semi_col.fullmatch(token) :
        print("SEMICOLON:", token, "on line:", lineNum)
        found_tokens.append(("SEMICOLON", token, lineNum))
    else :
        print("INVALID TOKEN:", token, "on line:", lineNum)

test_string = ""

delimiters = ['{', '}', '(', ')', ';']

# Keeping track of line number
line_num = 1

for char in source_code :
    if char == '\n' :
        line_num += 1
    # First check if we've reached whitespace
    if char.isspace() :
        # We've reached whitespace, this absolutely signals the end of a token
        if test_string :
            # Do comparisons
            checkToken(test_string, line_num)
            test_string = ""
        continue
    # Now check if we've reached a delimiter listed above
    if char in delimiters :
        if test_string :
            checkToken(test_string, line_num)
            test_string = ""
        checkToken(char, line_num)
        continue

    test_string += char

# If there's a token at the end with no delimiter after, check for it
# This would mean a compilation error because the syntax is wrong anyways
if test_string :
    checkToken(test_string, line_num)

# Close the source file
source_file.close()

# Shows the found tokens for the parser
print(found_tokens)

# Dump the tokens into a json file
with open("tokens.json", "w") as tokenFile :
    json.dump(found_tokens, tokenFile)

tokenFile.close()


