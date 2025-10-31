#!/bin/bash

# Testing our parser against the invalid programs in chapter 1 tests
for file in *.c; do
    echo "----------------------------------"
    echo "Testing parser against: $file"
    python lexer.py $file
    python parser.py
done

echo "----------------------------------"