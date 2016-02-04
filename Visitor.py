from gen.LanguageVisitor import LanguageVisitor
from gen.LanguageParser import LanguageParser


class Visitor(LanguageVisitor):

    # Type constants
    BOOL = 0
    INT = 1
    STRING = 2
    UNION = 3
    PRIMITIVE = (0, 1)

    def __init__(self):
        self.tokens = {}
        # TODO: add tables of names of functions, threads and variables
        with open("gen/LanguageLexer.tokens", 'r') as f:
            for line in f:
                if 'T__' not in line and "'" not in line:
                    token_name, token_num = line[:-1].split('=')
                    self.tokens[int(token_num)] = token_name
    
    def visitTerminal(self, node):
        print('|   ' + node.getText())

    def visitMul(self, ctx: LanguageParser.MulContext):
        return super().visitMul(ctx)

    def visitExpression(self, ctx: LanguageParser.ExpressionContext):
        # TODO: assignment and check children
        expr_type, code = self.visitAndExpr(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in self.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                if ctx.getChild(2 * i + 1).getText() != '||':
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitAndExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in self.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = expr_type or next_expr_type
                code += next_expr_code + ['ior']
        return expr_type, code

    def visitVarType(self, ctx: LanguageParser.VarTypeContext):
        return super().visitVarType(ctx)

    def visitCallArguments(self, ctx: LanguageParser.CallArgumentsContext):
        return super().visitCallArguments(ctx)

    def visitCondition(self, ctx: LanguageParser.ConditionContext):
        return super().visitCondition(ctx)

    def visitTreadCall(self, ctx: LanguageParser.TreadCallContext):
        return super().visitTreadCall(ctx)

    def visitArguments(self, ctx: LanguageParser.ArgumentsContext):
        return super().visitArguments(ctx)

    def visitFunctionDefinition(self, ctx: LanguageParser.FunctionDefinitionContext):
        return super().visitFunctionDefinition(ctx)

    def visitCompExpr(self, ctx: LanguageParser.CompExprContext):
        # TODO: check children
        expr_type, code = self.visitArithmExpr(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in self.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                if ctx.getChild(2 * i + 1).getText() not in ('==' | '!=' | '>' | '<' | '>=' | '<='):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitAndExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in self.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = expr_type or next_expr_type
                code += next_expr_code + ['ior']
        return expr_type, code

    def visitWrite(self, ctx: LanguageParser.WriteContext):
        # TODO: check children
        expr_type, expr_code = self.visitExpression(ctx.getChild(1))
        if expr_type == self.BOOL:
            expr_type = 'B'
        elif expr_type == self.INT:
            expr_type = 'I'
        elif expr_type == self.STRING:
            expr_type = 'Ljava/lang/String;'
        else:
            print('error')  # TODO: handle error
            exit(0)
        return ['getstatic java/lang/System/out Ljava/io/PrintStream'] + expr_code + \
               ['invokevirtual java/io/PrintStream/print(' + expr_type + ')V']

    def visitAndExpr(self, ctx: LanguageParser.AndExprContext):
        # TODO: check children
        expr_type, code = self.visitCompExpr(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in self.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                # TODO check that child is '||'
                if ctx.getChild(2 * i + 1).getText() != '&&':
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitCompExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in self.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = expr_type or next_expr_type
                code += next_expr_code + ['iand']
        return expr_type, code

    def visitReturnValue(self, ctx: LanguageParser.ReturnValueContext):
        return super().visitReturnValue(ctx)

    def visitVarDeclaration(self, ctx: LanguageParser.VarDeclarationContext):
        return super().visitVarDeclaration(ctx)

    def visitProgram(self, ctx: LanguageParser.ProgramContext):
        return super().visitProgram(ctx)

    def visitFunction(self, ctx: LanguageParser.FunctionContext):
        return super().visitFunction(ctx)

    def visitComment(self, ctx: LanguageParser.CommentContext):
        return super().visitComment(ctx)

    def visitFuncCall(self, ctx: LanguageParser.FuncCallContext):
        return super().visitFuncCall(ctx)

    def visitVar(self, ctx: LanguageParser.VarContext):
        return super().visitVar(ctx)

    def visitFuncType(self, ctx: LanguageParser.FuncTypeContext):
        return super().visitFuncType(ctx)

    def visitThread(self, ctx: LanguageParser.ThreadContext):
        return super().visitThread(ctx)

    def visitArithmExpr(self, ctx: LanguageParser.ArithmExprContext):
        return super().visitArithmExpr(ctx)

    def visitBlock(self, ctx: LanguageParser.BlockContext):
        return super().visitBlock(ctx)

    def visitAssignment(self, ctx: LanguageParser.AssignmentContext):
        return super().visitAssignment(ctx)

    def visitArgument(self, ctx: LanguageParser.ArgumentContext):
        return super().visitArgument(ctx)

    def visitUnionDeclaration(self, ctx: LanguageParser.UnionDeclarationContext):
        return super().visitUnionDeclaration(ctx)

    def visitCycle(self, ctx: LanguageParser.CycleContext):
        return super().visitCycle(ctx)

    def visitFunctionDeclaration(self, ctx: LanguageParser.FunctionDeclarationContext):
        return super().visitFunctionDeclaration(ctx)

    def visitRead(self, ctx: LanguageParser.ReadContext):
        return super().visitRead(ctx)

    def visitSummand(self, ctx: LanguageParser.SummandContext):
        return super().visitSummand(ctx)

    def visitCommand(self, ctx: LanguageParser.CommandContext):
        return super().visitCommand(ctx)
