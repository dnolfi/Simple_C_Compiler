Developing a simple C compiler in Python. This project is based on the book "Writing a C Compiler" by Nora Sandler. Other resources used for this project are "Compilers: Principles, Techniques and Tools" by Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman, ChatGPT
and web resources on Python and compiler development for theory references.

The compiler currently can compile a simple C program that just returns an exit code (see return_2.c). It can handle returning any integer (0, 100, -1, etc).
Currently, the compiler expects "void" to be between the main function call parentheises.

To run the compiler with the example source file (or replace return_2c with your own source file), use the following command in the terminal:

python compilerDriver.py return_2.c return_2

The compiler will successfully produce an x64 NASM assembly file and will assemble and link the file with NASM.

To verify that the return code is the correct one, run:

echo $?

