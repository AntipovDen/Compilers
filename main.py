import sys
from antlr4 import *

from VisitorPrinter import VisitorPrinter
from Visitor import Visitor
from gen.LanguageLexer import LanguageLexer
from gen.LanguageParser import LanguageParser

from os import getcwd
from os.path import join

if len(sys.argv) < 2 or sys.argc[1] == '-p' and len(sys.argv) < 3:
    print("Usage: python3 " + sys.argv[0] + " [-p] filename")
    exit(0)
else:
    if sys.argv == '-p':
        filename = sys.argv[1]
        to_print = True
    else:
        filename = sys.argv[0]

    input_stream = FileStream(join(getcwd(), filename))
    lexer = LanguageLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LanguageParser(stream)
    tree = parser.program()
    v = Visitor("helloworld")
    # v = VisitorPrinter()
    v.visit(tree)
    with open("out/helloworld.j", 'w') as f:
        for s in v.build_code():
            f.write(s)
            f.write('\n')
