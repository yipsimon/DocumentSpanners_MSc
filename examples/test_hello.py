import sys
from antlr4 import *
from HelloLexer import HelloLexer
from HelloParser import HelloParser

input = FileStream('input.txt')
lexer = HelloLexer(input)
stream = CommonTokenStream(lexer)
parser = HelloParser(stream)
tree = parser.r()
print (tree.toStringTree(recog=parser))
	

