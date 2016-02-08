# Generated from /home/dantipov/PycharmProjects/Compilers/Language.g4 by ANTLR 4.5.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LanguageParser import LanguageParser
else:
    from LanguageParser import LanguageParser

# This class defines a complete listener for a parse tree produced by LanguageParser.
class LanguageListener(ParseTreeListener):

    # Enter a parse tree produced by LanguageParser#program.
    def enterProgram(self, ctx:LanguageParser.ProgramContext):
        pass

    # Exit a parse tree produced by LanguageParser#program.
    def exitProgram(self, ctx:LanguageParser.ProgramContext):
        pass


    # Enter a parse tree produced by LanguageParser#function.
    def enterFunction(self, ctx:LanguageParser.FunctionContext):
        pass

    # Exit a parse tree produced by LanguageParser#function.
    def exitFunction(self, ctx:LanguageParser.FunctionContext):
        pass


    # Enter a parse tree produced by LanguageParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:LanguageParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by LanguageParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:LanguageParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by LanguageParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:LanguageParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by LanguageParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:LanguageParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by LanguageParser#funcType.
    def enterFuncType(self, ctx:LanguageParser.FuncTypeContext):
        pass

    # Exit a parse tree produced by LanguageParser#funcType.
    def exitFuncType(self, ctx:LanguageParser.FuncTypeContext):
        pass


    # Enter a parse tree produced by LanguageParser#varType.
    def enterVarType(self, ctx:LanguageParser.VarTypeContext):
        pass

    # Exit a parse tree produced by LanguageParser#varType.
    def exitVarType(self, ctx:LanguageParser.VarTypeContext):
        pass


    # Enter a parse tree produced by LanguageParser#arguments.
    def enterArguments(self, ctx:LanguageParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by LanguageParser#arguments.
    def exitArguments(self, ctx:LanguageParser.ArgumentsContext):
        pass


    # Enter a parse tree produced by LanguageParser#argument.
    def enterArgument(self, ctx:LanguageParser.ArgumentContext):
        pass

    # Exit a parse tree produced by LanguageParser#argument.
    def exitArgument(self, ctx:LanguageParser.ArgumentContext):
        pass


    # Enter a parse tree produced by LanguageParser#block.
    def enterBlock(self, ctx:LanguageParser.BlockContext):
        pass

    # Exit a parse tree produced by LanguageParser#block.
    def exitBlock(self, ctx:LanguageParser.BlockContext):
        pass


    # Enter a parse tree produced by LanguageParser#thread.
    def enterThread(self, ctx:LanguageParser.ThreadContext):
        pass

    # Exit a parse tree produced by LanguageParser#thread.
    def exitThread(self, ctx:LanguageParser.ThreadContext):
        pass


    # Enter a parse tree produced by LanguageParser#command.
    def enterCommand(self, ctx:LanguageParser.CommandContext):
        pass

    # Exit a parse tree produced by LanguageParser#command.
    def exitCommand(self, ctx:LanguageParser.CommandContext):
        pass


    # Enter a parse tree produced by LanguageParser#varDeclaration.
    def enterVarDeclaration(self, ctx:LanguageParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by LanguageParser#varDeclaration.
    def exitVarDeclaration(self, ctx:LanguageParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by LanguageParser#unionDeclaration.
    def enterUnionDeclaration(self, ctx:LanguageParser.UnionDeclarationContext):
        pass

    # Exit a parse tree produced by LanguageParser#unionDeclaration.
    def exitUnionDeclaration(self, ctx:LanguageParser.UnionDeclarationContext):
        pass


    # Enter a parse tree produced by LanguageParser#assignment.
    def enterAssignment(self, ctx:LanguageParser.AssignmentContext):
        pass

    # Exit a parse tree produced by LanguageParser#assignment.
    def exitAssignment(self, ctx:LanguageParser.AssignmentContext):
        pass


    # Enter a parse tree produced by LanguageParser#expression.
    def enterExpression(self, ctx:LanguageParser.ExpressionContext):
        pass

    # Exit a parse tree produced by LanguageParser#expression.
    def exitExpression(self, ctx:LanguageParser.ExpressionContext):
        pass


    # Enter a parse tree produced by LanguageParser#andExpr.
    def enterAndExpr(self, ctx:LanguageParser.AndExprContext):
        pass

    # Exit a parse tree produced by LanguageParser#andExpr.
    def exitAndExpr(self, ctx:LanguageParser.AndExprContext):
        pass


    # Enter a parse tree produced by LanguageParser#compExpr.
    def enterCompExpr(self, ctx:LanguageParser.CompExprContext):
        pass

    # Exit a parse tree produced by LanguageParser#compExpr.
    def exitCompExpr(self, ctx:LanguageParser.CompExprContext):
        pass


    # Enter a parse tree produced by LanguageParser#arithmExpr.
    def enterArithmExpr(self, ctx:LanguageParser.ArithmExprContext):
        pass

    # Exit a parse tree produced by LanguageParser#arithmExpr.
    def exitArithmExpr(self, ctx:LanguageParser.ArithmExprContext):
        pass


    # Enter a parse tree produced by LanguageParser#summand.
    def enterSummand(self, ctx:LanguageParser.SummandContext):
        pass

    # Exit a parse tree produced by LanguageParser#summand.
    def exitSummand(self, ctx:LanguageParser.SummandContext):
        pass


    # Enter a parse tree produced by LanguageParser#mul.
    def enterMul(self, ctx:LanguageParser.MulContext):
        pass

    # Exit a parse tree produced by LanguageParser#mul.
    def exitMul(self, ctx:LanguageParser.MulContext):
        pass


    # Enter a parse tree produced by LanguageParser#var.
    def enterVar(self, ctx:LanguageParser.VarContext):
        pass

    # Exit a parse tree produced by LanguageParser#var.
    def exitVar(self, ctx:LanguageParser.VarContext):
        pass


    # Enter a parse tree produced by LanguageParser#funcCall.
    def enterFuncCall(self, ctx:LanguageParser.FuncCallContext):
        pass

    # Exit a parse tree produced by LanguageParser#funcCall.
    def exitFuncCall(self, ctx:LanguageParser.FuncCallContext):
        pass


    # Enter a parse tree produced by LanguageParser#callArguments.
    def enterCallArguments(self, ctx:LanguageParser.CallArgumentsContext):
        pass

    # Exit a parse tree produced by LanguageParser#callArguments.
    def exitCallArguments(self, ctx:LanguageParser.CallArgumentsContext):
        pass


    # Enter a parse tree produced by LanguageParser#treadCall.
    def enterTreadCall(self, ctx:LanguageParser.TreadCallContext):
        pass

    # Exit a parse tree produced by LanguageParser#treadCall.
    def exitTreadCall(self, ctx:LanguageParser.TreadCallContext):
        pass


    # Enter a parse tree produced by LanguageParser#condition.
    def enterCondition(self, ctx:LanguageParser.ConditionContext):
        pass

    # Exit a parse tree produced by LanguageParser#condition.
    def exitCondition(self, ctx:LanguageParser.ConditionContext):
        pass


    # Enter a parse tree produced by LanguageParser#cycle.
    def enterCycle(self, ctx:LanguageParser.CycleContext):
        pass

    # Exit a parse tree produced by LanguageParser#cycle.
    def exitCycle(self, ctx:LanguageParser.CycleContext):
        pass


    # Enter a parse tree produced by LanguageParser#read.
    def enterRead(self, ctx:LanguageParser.ReadContext):
        pass

    # Exit a parse tree produced by LanguageParser#read.
    def exitRead(self, ctx:LanguageParser.ReadContext):
        pass


    # Enter a parse tree produced by LanguageParser#write.
    def enterWrite(self, ctx:LanguageParser.WriteContext):
        pass

    # Exit a parse tree produced by LanguageParser#write.
    def exitWrite(self, ctx:LanguageParser.WriteContext):
        pass


    # Enter a parse tree produced by LanguageParser#returnValue.
    def enterReturnValue(self, ctx:LanguageParser.ReturnValueContext):
        pass

    # Exit a parse tree produced by LanguageParser#returnValue.
    def exitReturnValue(self, ctx:LanguageParser.ReturnValueContext):
        pass


    # Enter a parse tree produced by LanguageParser#comment.
    def enterComment(self, ctx:LanguageParser.CommentContext):
        pass

    # Exit a parse tree produced by LanguageParser#comment.
    def exitComment(self, ctx:LanguageParser.CommentContext):
        pass


