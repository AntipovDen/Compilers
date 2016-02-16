# Generated from /home/dantipov/PycharmProjects/Compilers/Language.g4 by ANTLR 4.5.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LanguageParser import LanguageParser
else:
    from LanguageParser import LanguageParser

# This class defines a complete generic visitor for a parse tree produced by LanguageParser.

class LanguageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LanguageParser#program.
    def visitProgram(self, ctx:LanguageParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#function.
    def visitFunction(self, ctx:LanguageParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:LanguageParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:LanguageParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#funcType.
    def visitFuncType(self, ctx:LanguageParser.FuncTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#varType.
    def visitVarType(self, ctx:LanguageParser.VarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#arguments.
    def visitArguments(self, ctx:LanguageParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#argument.
    def visitArgument(self, ctx:LanguageParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#block.
    def visitBlock(self, ctx:LanguageParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#thread.
    def visitThread(self, ctx:LanguageParser.ThreadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#command.
    def visitCommand(self, ctx:LanguageParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#varDeclaration.
    def visitVarDeclaration(self, ctx:LanguageParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#unionDeclaration.
    def visitUnionDeclaration(self, ctx:LanguageParser.UnionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#unionField.
    def visitUnionField(self, ctx:LanguageParser.UnionFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#assignment.
    def visitAssignment(self, ctx:LanguageParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#expression.
    def visitExpression(self, ctx:LanguageParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#andExpr.
    def visitAndExpr(self, ctx:LanguageParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#compExpr.
    def visitCompExpr(self, ctx:LanguageParser.CompExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#arithmExpr.
    def visitArithmExpr(self, ctx:LanguageParser.ArithmExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#summand.
    def visitSummand(self, ctx:LanguageParser.SummandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#castedMul.
    def visitCastedMul(self, ctx:LanguageParser.CastedMulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#mul.
    def visitMul(self, ctx:LanguageParser.MulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#var.
    def visitVar(self, ctx:LanguageParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#funcCall.
    def visitFuncCall(self, ctx:LanguageParser.FuncCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#callArguments.
    def visitCallArguments(self, ctx:LanguageParser.CallArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#treadCall.
    def visitTreadCall(self, ctx:LanguageParser.TreadCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#condition.
    def visitCondition(self, ctx:LanguageParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#cycle.
    def visitCycle(self, ctx:LanguageParser.CycleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#read.
    def visitRead(self, ctx:LanguageParser.ReadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#write.
    def visitWrite(self, ctx:LanguageParser.WriteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#returnValue.
    def visitReturnValue(self, ctx:LanguageParser.ReturnValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#comment.
    def visitComment(self, ctx:LanguageParser.CommentContext):
        return self.visitChildren(ctx)



del LanguageParser