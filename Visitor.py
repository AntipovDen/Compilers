from gen.LanguageVisitor import LanguageVisitor
from gen.LanguageParser import LanguageParser


class Visitor(LanguageVisitor):

    # Type constants
    BOOL = 0
    INT = 1
    STRING = 2
    UNION = 3
    VOID = 4
    STRING_ARR = 5
    PRIMITIVE = (0, 1)

    def __init__(self):
        self.tokens = {}
        # TODO: add tables of names of functions, threads and variables
        with open("gen/LanguageLexer.tokens", 'r') as f:
            for line in f:
                if 'T__' not in line and "'" not in line:
                    token_name, token_num = line[:-1].split('=')
                    self.tokens[int(token_num)] = token_name
        self.op_name = {'==': 'eq', '!=': 'ne', '>': 'gt', '<': 'lt', '>=': 'ge', '<=': 'le'}
        self.label_num = 0
        self.local_variable_num = -1
        # here will be stored methodName: retType, [arguments], [code lines]
        self.methods = {'main': [self.VOID, [(self.STRING_ARR, 'args')], []]}
        self.threads = {}  # here will be stored threadName: [arguments], [thread code lines])
        self.fields = {}  # here will be stored varName: varType
        self.current_method = 'main'
        self.visible_vars = {} # varName: type, number

    def getNextLabelNum(self):
        self.label_num += 1
        return self.label_num

    def getNextLocalVar(self):
        self.local_variable_num += 1
        return self.local_variable_num
    def visitTerminal(self, node):
        print('|   ' + node.getText())

    def whichType(self, int):
        return 'V' if int == self.VOID \
                else 'B' if int == self.BOOL \
                else 'I' if int == self.INT  \
                else 'Ljava/lang/String;' if int == self.STRING  \
                else '[Ljava/lang/String;' if int == self.STRING_ARR  \
                else None

    def buildCode(self, classname):
        code = []
        #TODO fields, threads
        code.append(".source " + classname + ".dc")
        code.append(".class " + classname)
        code.append(".super java/lang/Object")
        code.append("")
        for method in self.methods:
            method_params = self.methods[method]
            method_type = self.whichType(method_params[0])
            args = ""
            for arg in method_params[1]:
                args += self.whichType(arg[0])
            code.append(".method public static " + method + "(" + args + ")" + method_type)
            code += method_params[2]
            if method_type == 'V':
                code.append("return")
            code.append(".end method")
            code.append("")
        return code

    def visitProgram(self, ctx: LanguageParser.ProgramContext):
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if not hasattr(child, 'getRuleIndex'):
                print("error")
                exit(0)  # TODO: handle error
            if child.getRuleIndex() != LanguageParser.RULE_comment:
                child.accept(self)

    def visitCommand(self, ctx: LanguageParser.CommandContext):
        child = ctx.getChild(0)
        if child.getRuleIndex() == LanguageParser.RULE_write:
            self.methods[self.current_method][2] += self.visitWrite(child)

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

    def visitCompExpr(self, ctx: LanguageParser.CompExprContext):
        # TODO: check children
        expr_type, code = self.visitArithmExpr(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in self.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('==', '!=', '>', '<', '>=', '<='):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitArithmExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in self.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error


                expr_type = self.BOOL
                true_label = 'Label' + self.getNextLabelNum()
                exit_label = 'Label' + self.getNextLabelNum()
                code += next_expr_code + ['if_icmp' + self.op_name[op] + true_label,
                                          'iconst_0', 'goto' + exit_label, true_label + ':',
                                          'iconst_1', exit_label + ':']
        return expr_type, code

    def visitArithmExpr(self, ctx: LanguageParser.ArithmExprContext):
        # TODO: check children
        expr_type, code = self.visitSummand(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in self.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('+', '-'):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitSummand(ctx.getChild(2 * i + 2))
                if next_expr_type not in self.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = self.INT
                code += next_expr_code + ['iadd' if op == '+' else 'isub']
        return expr_type, code

    def visitSummand(self, ctx: LanguageParser.SummandContext):
        # TODO: check children
        expr_type, code = self.visitMul(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in self.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('*', '/', '%'):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitMul(ctx.getChild(2 * i + 2))
                if next_expr_type not in self.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = self.INT
                code += next_expr_code
                if op == '*':
                    code.append('imul')
                elif op == '/':
                    code.append('idiv')
                else:
                    code.append('irem')
        return expr_type, code

    def visitMul(self, ctx: LanguageParser.MulContext):
        if ctx.getChildCount() == 3:
            if ctx.getChild(0).getText() != '(' or  \
               ctx.getChild(2).getText() != ')' or \
               not hasattr(ctx.getChild(1), 'getRuleIndex') or \
               ctx.getChild(1).getRuleIndex == LanguageParser.RULE_expression:
                print('error')
                exit(0)  # TODO: handle error
            return self.visitExpression(ctx.getChild(1))

        child = ctx.getChild(0)
        if hasattr(child, 'getRuleIndex'):
            if child.getRuleIndex == LanguageParser.RULE_var:
                return self.visitVar(child)
            elif child.getRuleIndex == LanguageParser.RULE_funcCall:
                return self.visitFuncCall(child)
            else:
                print("error")
                exit(0)  # TODO: handle error
        else:
            if child.getSymbol().type == LanguageParser.Bool:
                return self.BOOL, ['iconst_0' if child.getText() == 'false' else 'iconst_1']
            elif child.getSymbol().type == LanguageParser.Integer:
                return self.INT, ['ldc ' + child.getText()]
            elif child.getSymbol().type == LanguageParser.String:
                return  self.STRING, ['ldc ' + child.getText()]

 # everithing below isn't yet realized

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

    def visitReturnValue(self, ctx: LanguageParser.ReturnValueContext):
        return super().visitReturnValue(ctx)

    def visitVarDeclaration(self, ctx: LanguageParser.VarDeclarationContext):
        return super().visitVarDeclaration(ctx)

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

