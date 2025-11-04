import lexer as lex
import parser as prse
import asmgen as gen
import subprocess
import sys  # This is to read the cmd line args
import json

if  len(sys.argv) < 3 :
    print("Error: Must provide source file in command line arguments.")
    print("Error: Must provide name of executable in command line args")
    exit(1)    

if not sys.argv[1].endswith('.c') :
    print("Lexer Error: Input must be a .c file for compilation. Compilation aborted.")
    exit(1)

executableName = sys.argv[2]

# Calls the preprocessor, lexer, parser and assembly generator to compile a simple C source program
# Open the source file we passed as our argument, after checking to make sure the file is a .c file!
source_file = open(sys.argv[1])

lex.runLexer(source_file)

# Need to load our dictionary of tokens from the lexer step
with open('tokens.json', 'r') as tokenFile :
    tokens = json.load(tokenFile)

# Parser our tokens
parser = prse.Parser(tokens)
tree = parser.parseProgram()

# Now generate the code
cg = gen.CodeGenerator()
cg.traverseTree(tree)

# Now we need to write our asm to a file, assemble it and then we can run the executable
with open(f"{executableName}.s", "w") as f :
    for line in cg.asm :
        if line.startswith((";", ".")) or line.endswith(":") :
            f.write(f"{line}\n")
        else :
            f.write(f"\t{line}\n")

# Now need to assemble and link our assembly file to produce an executable
asmFile = f"{executableName}.s"
objFile = f"{executableName}.o"

# Assemble
try:
    subprocess.run(["nasm", "-f", "elf64", asmFile, "-o", objFile], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError as e:
    print("Error: NASM assembly failed")
    print(e.stderr.decode())
    exit(1)

# Link
try:
    subprocess.run(["ld", objFile, "-o", executableName], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError as e:
    print("Error: Linking failed")
    print(e.stderr.decode())
    exit(1)

print(f"Complation successful. Run ./{executableName}")

