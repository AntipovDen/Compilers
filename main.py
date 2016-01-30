from antlr4 import *
from gen.LanguageLexer import LanguageLexer
from gen.LanguageParser import LanguageParser
from gen.LanguageListener import LanguageListener

from example.startPrinter import StartPrinter

input = FileStream("input.txt")
lexer = LanguageLexer(input)
stream = CommonTokenStream(lexer)
parser = LanguageParser(stream)
tree = parser.program()

class WalkPrinter(LanguageListener):
    def exitReturnValue(self, ctx: LanguageParser.ReturnValueContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitCallArguments(self, ctx: LanguageParser.CallArgumentsContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitCycle(self, ctx: LanguageParser.CycleContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitUnionDeclaration(self, ctx: LanguageParser.UnionDeclarationContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitSummand(self, ctx: LanguageParser.SummandContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitVarDeclaration(self, ctx: LanguageParser.VarDeclarationContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterMul(self, ctx: LanguageParser.MulContext):
        print('\t' * self.tabs + 'Mul:' + ctx.getText() + '{')
        self.tabs += 1

    def enterVarDeclaration(self, ctx: LanguageParser.VarDeclarationContext):
        print('\t' * self.tabs + 'VarDeclaration:' + ctx.getText() + '{')
        self.tabs += 1

    def enterAssignment(self, ctx: LanguageParser.AssignmentContext):
        print('\t' * self.tabs + 'Assignment:' + ctx.getText() + '{')
        self.tabs += 1

    def exitWrite(self, ctx: LanguageParser.WriteContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterCondition(self, ctx: LanguageParser.ConditionContext):
        print('\t' * self.tabs + 'Condition:' + ctx.getText() + '{')
        self.tabs += 1

    def exitArithmExpr(self, ctx: LanguageParser.ArithmExprContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitExpression(self, ctx: LanguageParser.ExpressionContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitAssignment(self, ctx: LanguageParser.AssignmentContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterVar(self, ctx: LanguageParser.VarContext):
        print('\t' * self.tabs + 'Var:' + ctx.getText() + '{')
        self.tabs += 1

    def exitCondition(self, ctx: LanguageParser.ConditionContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterCycle(self, ctx: LanguageParser.CycleContext):
        print('\t' * self.tabs + 'Cycle:' + ctx.getText() + '{')
        self.tabs += 1

    def enterCallArguments(self, ctx: LanguageParser.CallArgumentsContext):
        print('\t' * self.tabs + 'CallArguments:' + ctx.getText() + '{')
        self.tabs += 1

    def exitFuncCall(self, ctx: LanguageParser.FuncCallContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterUnionDeclaration(self, ctx: LanguageParser.UnionDeclarationContext):
        print('\t' * self.tabs + 'UnionDeclaration:' + ctx.getText() + '{')
        self.tabs += 1

    def enterWrite(self, ctx: LanguageParser.WriteContext):
        print('\t' * self.tabs + 'Write:' + ctx.getText() + '{')
        self.tabs += 1

    def exitMul(self, ctx: LanguageParser.MulContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterExpression(self, ctx: LanguageParser.ExpressionContext):
        print('\t' * self.tabs + 'Expression:' + ctx.getText() + '{')
        self.tabs += 1

    def exitRead(self, ctx: LanguageParser.ReadContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterReturnValue(self, ctx: LanguageParser.ReturnValueContext):
        print('\t' * self.tabs + 'ReturnValue:' + ctx.getText() + '{')
        self.tabs += 1

    def enterRead(self, ctx: LanguageParser.ReadContext):
        print('\t' * self.tabs + 'Read:' + ctx.getText() + '{')
        self.tabs += 1

    def enterCompExpr(self, ctx: LanguageParser.CompExprContext):
        print('\t' * self.tabs + 'CompExpr:' + ctx.getText() + '{')
        self.tabs += 1

    def enterFuncCall(self, ctx: LanguageParser.FuncCallContext):
        print('\t' * self.tabs + 'FuncCall:' + ctx.getText() + '{')
        self.tabs += 1

    def exitVar(self, ctx: LanguageParser.VarContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitAndExpr(self, ctx: LanguageParser.AndExprContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitCompExpr(self, ctx: LanguageParser.CompExprContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterArithmExpr(self, ctx: LanguageParser.ArithmExprContext):
        print('\t' * self.tabs + 'ArithmExpr:' + ctx.getText() + '{')
        self.tabs += 1

    def enterSummand(self, ctx: LanguageParser.SummandContext):
        print('\t' * self.tabs + 'Summand:' + ctx.getText() + '{')
        self.tabs += 1

    def exitTreadCall(self, ctx: LanguageParser.TreadCallContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterAndExpr(self, ctx: LanguageParser.AndExprContext):
        print('\t' * self.tabs + 'AndExpr:' + ctx.getText() + '{')
        self.tabs += 1

    def enterTreadCall(self, ctx: LanguageParser.TreadCallContext):
        print('\t' * self.tabs + 'TreadCall:' + ctx.getText() + '{')
        self.tabs += 1

    def __init__(self):
        self.tabs = 0

    def enterArgument(self, ctx: LanguageParser.ArgumentContext):
        print('\t' * self.tabs + 'Argument:' + ctx.getText() + '{')
        self.tabs += 1

    def exitProgram(self, ctx: LanguageParser.ProgramContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterThread(self, ctx: LanguageParser.ThreadContext):
        print('\t' * self.tabs + 'Thread:' + ctx.getText() + '{')
        self.tabs += 1

    def enterCommand(self, ctx: LanguageParser.CommandContext):
        print('\t' * self.tabs + 'Command:' + ctx.getText() + '{')
        self.tabs += 1

    def enterFunction(self, ctx: LanguageParser.FunctionContext):
        print('\t' * self.tabs + 'Function:' + ctx.getText() + '{')
        self.tabs += 1

    def enterBlock(self, ctx: LanguageParser.BlockContext):
        print('\t' * self.tabs + 'Block:' + ctx.getText() + '{')
        self.tabs += 1

    def exitArguments(self, ctx: LanguageParser.ArgumentsContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitThread(self, ctx: LanguageParser.ThreadContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterFuncType(self, ctx: LanguageParser.FuncTypeContext):
        print('\t' * self.tabs + 'FuncType:' + ctx.getText() + '{')
        self.tabs += 1

    def exitVarType(self, ctx: LanguageParser.VarTypeContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterArguments(self, ctx: LanguageParser.ArgumentsContext):
        print('\t' * self.tabs + 'Arguments:' + ctx.getText() + '{')
        self.tabs += 1

    def exitCommand(self, ctx: LanguageParser.CommandContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterFunctionDeclaration(self, ctx: LanguageParser.FunctionDeclarationContext):
        print('\t' * self.tabs + 'FunctionDeclaration:' + ctx.getText() + '{')
        self.tabs += 1

    def exitFunction(self, ctx: LanguageParser.FunctionContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitFuncType(self, ctx: LanguageParser.FuncTypeContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterProgram(self, ctx: LanguageParser.ProgramContext):
        print('\t' * self.tabs + 'Program:' + ctx.getText() + '{')
        self.tabs += 1

    def enterVarType(self, ctx: LanguageParser.VarTypeContext):
        print('\t' * self.tabs + 'VarType:' + ctx.getText() + '{')
        self.tabs += 1

    def exitFunctionDefinition(self, ctx: LanguageParser.FunctionDefinitionContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitFunctionDeclaration(self, ctx: LanguageParser.FunctionDeclarationContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitBlock(self, ctx: LanguageParser.BlockContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def exitArgument(self, ctx: LanguageParser.ArgumentContext):
        self.tabs -= 1
        print('\t' * self.tabs + '}')

    def enterFunctionDefinition(self, ctx: LanguageParser.FunctionDefinitionContext):
        print('\t' * self.tabs + 'FunctionDefinition:' + ctx.getText() + '{')
        self.tabs += 1


walker = ParseTreeWalker()
walker.walk(WalkPrinter(), tree)