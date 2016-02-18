import sys
from antlr4 import *

from VisitorPrinter import VisitorPrinter
from Visitor import Visitor
from gen.LanguageLexer import LanguageLexer
from gen.LanguageParser import LanguageParser

from os import getcwd
from os.path import join


if len(sys.argv) < 2 or sys.argv[1] == '-p' and len(sys.argv) < 3:
    print("Usage: python3 " + sys.argv[0] + " [-p] filename")
    exit(0)
if sys.argv[1] == '-p':
    filename = sys.argv[2]
    to_print = True
else:
    filename = sys.argv[1]
    to_print = False


input_stream = FileStream(join(getcwd(), filename))
lexer = LanguageLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = LanguageParser(stream)
tree = parser.program()
classname = filename.split('/')[-1].split('.')[0]

if to_print:
    v = VisitorPrinter()
    v.visit(tree)
v = Visitor(classname)
v.visit(tree)
with open("out/" + classname + ".j", 'w') as f:
    for s in v.build_code():
        f.write(s)
        f.write('\n')
