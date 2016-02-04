from antlr4 import *

from VisitorPrinter import VisitorPrinter
from gen.LanguageLexer import LanguageLexer
from gen.LanguageParser import LanguageParser

from os import listdir
from os.path import join


for filename in listdir("examples"):
    input_stream = FileStream(join("examples", filename))
    lexer = LanguageLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LanguageParser(stream)
    tree = parser.program()
    v = VisitorPrinter()
    v.visit(tree)
    print('------------------------------------------------------------------------------------')
