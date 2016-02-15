from gen.LanguageVisitor import LanguageVisitor
from gen.LanguageParser import LanguageParser


class VisitorPrinter(LanguageVisitor):
    def __init__(self):
        self.tabs = 0

    def visitTerminal(self, node):
        print('|   ' * self.tabs + node.getText())

    def visitCastedMul(self, ctx: LanguageParser.CastedMulContext):
        print('|   ' * self.tabs + "CastedMul")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1

    def visitCommand(self, ctx: LanguageParser.CommandContext):
        print('|   ' * self.tabs + "Command")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitCallArguments(self, ctx: LanguageParser.CallArgumentsContext):
        print('|   ' * self.tabs + "CallArguments")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitBlock(self, ctx: LanguageParser.BlockContext):
        print('|   ' * self.tabs + "Block")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitAssignment(self, ctx: LanguageParser.AssignmentContext):
        print('|   ' * self.tabs + "Assignment")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitFuncCall(self, ctx: LanguageParser.FuncCallContext):
        print('|   ' * self.tabs + "FuncCall")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitArgument(self, ctx: LanguageParser.ArgumentContext):
        print('|   ' * self.tabs + "Argument")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitVar(self, ctx: LanguageParser.VarContext):
        print('|   ' * self.tabs + "Var")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitVarType(self, ctx: LanguageParser.VarTypeContext):
        print('|   ' * self.tabs + "VarType")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitRead(self, ctx: LanguageParser.ReadContext):
        print('|   ' * self.tabs + "Read")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitFunction(self, ctx: LanguageParser.FunctionContext):
        print('|   ' * self.tabs + "Function")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitCompExpr(self, ctx: LanguageParser.CompExprContext):
        print('|   ' * self.tabs + "CompExpr")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitMul(self, ctx: LanguageParser.MulContext):
        print('|   ' * self.tabs + "Mul")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitFunctionDefinition(self, ctx: LanguageParser.FunctionDefinitionContext):
        print('|   ' * self.tabs + "FunctionDefinition")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitTreadCall(self, ctx: LanguageParser.TreadCallContext):
        print('|   ' * self.tabs + "TreadCall")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitComment(self, ctx: LanguageParser.CommentContext):
        print('|   ' * self.tabs + "Comment")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitCondition(self, ctx: LanguageParser.ConditionContext):
        print('|   ' * self.tabs + "Condition")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitUnionDeclaration(self, ctx: LanguageParser.UnionDeclarationContext):
        print('|   ' * self.tabs + "UnionDeclaration")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1

    def visitUnionField(self, ctx: LanguageParser.UnionFieldContext):
        print('|   ' * self.tabs + "UnionField")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1

    def visitArguments(self, ctx: LanguageParser.ArgumentsContext):
        print('|   ' * self.tabs + "Arguments")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitReturnValue(self, ctx: LanguageParser.ReturnValueContext):
        print('|   ' * self.tabs + "ReturnValue")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitThread(self, ctx: LanguageParser.ThreadContext):
        print('|   ' * self.tabs + "Thread")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitProgram(self, ctx: LanguageParser.ProgramContext):
        print('|   ' * self.tabs + "Program")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitFunctionDeclaration(self, ctx: LanguageParser.FunctionDeclarationContext):
        print('|   ' * self.tabs + "FunctionDeclaration")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitFuncType(self, ctx: LanguageParser.FuncTypeContext):
        print('|   ' * self.tabs + "FuncType")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitAndExpr(self, ctx: LanguageParser.AndExprContext):
        print('|   ' * self.tabs + "AndExpr")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitSummand(self, ctx: LanguageParser.SummandContext):
        print('|   ' * self.tabs + "Summand")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitExpression(self, ctx: LanguageParser.ExpressionContext):
        print('|   ' * self.tabs + "Expression")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitWrite(self, ctx: LanguageParser.WriteContext):
        print('|   ' * self.tabs + "Write")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitCycle(self, ctx: LanguageParser.CycleContext):
        print('|   ' * self.tabs + "Cycle")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitArithmExpr(self, ctx: LanguageParser.ArithmExprContext):
        print('|   ' * self.tabs + "ArithmExpr")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1


    def visitVarDeclaration(self, ctx: LanguageParser.VarDeclarationContext):
        print('|   ' * self.tabs + "VarDeclaration")
        self.tabs += 1
        super().visitChildren(ctx)
        self.tabs -= 1
