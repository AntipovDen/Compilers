from antlr4 import *

from Visitor import Visitor
from gen.LanguageLexer import LanguageLexer
from gen.LanguageParser import LanguageParser

from os import listdir
from os.path import join


for filename in listdir("examples"):
    input = FileStream(join("examples", filename))
    lexer = LanguageLexer(input)
    stream = CommonTokenStream(lexer)
    parser = LanguageParser(stream)
    tree = parser.program()
    Visitor().visit(tree)
    print('------------------------------------------------------------------------------------')