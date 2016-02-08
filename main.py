from antlr4 import *

from VisitorPrinter import VisitorPrinter
from Visitor import Visitor
from gen.LanguageLexer import LanguageLexer
from gen.LanguageParser import LanguageParser

from os import listdir
from os.path import join


# for filename in listdir("examples"):
input_stream = FileStream(join("examples", "helloworld.dc"))
lexer = LanguageLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = LanguageParser(stream)
tree = parser.program()
v = Visitor("helloworld")
# v = VisitorPrinter()
v.visit(tree)
with open("out/helloworld.j", 'w') as f:
    for s in v.buildCode():
        f.write(s)
        f.write('\n')