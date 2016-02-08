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
    OP_NAME = {'==': 'eq', '!=': 'ne', '>': 'gt', '<': 'lt', '>=': 'ge', '<=': 'le'}

    class Method:
        def __init__(self, return_type=-1, arguments=[], code=[], locals=[], stack_limit=0):
            self.return_type = return_type
            self.arguments = arguments
            self.code = code
            self.locals = locals
            self.stack_limit = stack_limit

    class Argument:
        def __init__(self, arg_type=-1, name=None):
            self.type = arg_type
            self.name = name

        def __eq__(self, other):
            return self.type == other.type
          
    class Variable:
        def __init__(self, var_type=-1, name=None, local_number=0):
            self.type = var_type
            self.name = name
            self.local_number = local_number

                            
    def __init__(self, classname):
        self.label_num = 0
        self.local_variable_num = -1
        self.current_method = 'main'
        self.methods = {'main': Visitor.Method(return_type=Visitor.VOID,
                                               arguments=[Visitor.Argument(arg_type=Visitor.STRING_ARR, name = 'args')],
                                               stack_limit=20)}
        self.fields = {}  # fields are stored as name: type
        self.visible_vars = [] # maps name: number
        self.classname = classname

    def getNextLabelNum(self):
        self.label_num += 1
        return str(self.label_num)

    def typeToString(self, int_type):
        return 'V' if int == Visitor.VOID \
                else 'Z' if int == Visitor.BOOL \
                else 'I' if int == Visitor.INT  \
                else 'Ljava/lang/String;' if int == Visitor.STRING  \
                else '[Ljava/lang/String;' if int == Visitor.STRING_ARR  \
                else None

    def typeFromParser(self, parser_type):
        return self.BOOL if parser_type == LanguageParser.BoolType \
            else self.INT if parser_type == LanguageParser.IntType \
            else self.STRING if parser_type == LanguageParser.StringType \
            else self.VOID if parser_type == LanguageParser.VoidType \
            else None

    def isVisible(self, var_name):
        for vis in self.visible_vars:
            if var_name in vis:
                return True
        return False

    def getVarNumber(self, var_name):
        for vis in self.visible_vars:
            if var_name in vis:
                return vis[var_name]
        return None

    def checkArguments(self, arguments1, arguments2):
        if len(arguments1) != len(arguments2):
            return False
        for i in range(len(arguments1)):
            if arguments1[i] != arguments2[i]:
                return False
        return True

    def buildCode(self):
        code = []
        #TODO threads
        code.append(".class " + self.classname)
        code.append(".super java/lang/Object")
        code.append("")
        for field in self.fields:
            code.append(".field public static " + field + ' ' + self.typeToString(self.fields[field]))
        code.append("")
        for method in self.methods:
            method_params = self.methods[method]
            method_type = self.typeToString(method_params.return_type)
            args = ""
            for arg in method_params.arguments:
                args += self.typeToString(arg.type)
            code.append(".method public static " + method + " : (" + args + ")" + method_type)
            code.append(".limit stack " + str(method_params.stack_limit))
            code.append(".limit locals " + str(len(method_params.locals) + len(method_params.arguments)))
            code += method_params.code
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
        rule_index = child.getRuleIndex()
        if rule_index == LanguageParser.RULE_write:
            self.methods[self.current_method].code += self.visitWrite(child)
        elif rule_index == LanguageParser.RULE_assignment:
            _, code = self.visitAssignment(child)
            self.methods[self.current_method].code += code[:-1]
        elif rule_index == LanguageParser.RULE_varDeclaration:
            self.visitVarDeclaration(child)

    def visitAssignment(self, ctx: LanguageParser.AssignmentContext):
        var_name = ctx.getChild(0).getText()
        if var_name in self.fields:
            expr_type, expr_code = self.visitExpression(ctx.getChild(2))
            var_type = self.fields[var_name]
            if expr_type != var_type and (expr_type not in self.PRIMITIVE or var_type not in self.PRIMITIVE):
                print("Can't assign " + self.typeToString(expr_type) + " to the " +
                      self.typeToString(var_type) + " variable " + var_name)
            expr_code.append("putstatic " + self.classname + '/' + var_name +
                                                          ' ' + self.typeToString(var_type))
            expr_code.append("getstatic " + self.classname + '/' + var_name +
                                                          ' ' + self.typeToString(var_type))
            return expr_type, expr_code
        elif self.isVisible(var_name):
            expr_type, expr_code = self.visitExpression(ctx.getChild(2))
            var_number = self.getVarNumber(var_name)
            var_type = self.methods[self.current_method].locals[var_number].type
            if expr_type != var_type and (expr_type not in self.PRIMITIVE or var_type not in self.PRIMITIVE):
                print("Can't assign " + self.typeToString(expr_type) + " to the " +
                      self.typeToString(var_type) + " variable " + var_name)
            if var_type in Visitor.PRIMITIVE:
                expr_code.append("iload " + str(var_number))
                expr_code.append("istore " + str(var_number))
            elif var_type == Visitor.STRING:
                expr_code.append("aload " + str(var_number))
                expr_code.append("astore " + str(var_number))
        else:
            print("No such visible variable: " + var_name)
            exit(0)

    def visitVarDeclaration(self, ctx: LanguageParser.VarDeclarationContext):
        # TODO:
        # 1) check varname in local variables (or fields if we are in the main method)
        # 2) add varname to local variables or to the method fields
        # 3) if there is an assignment, do it.
        var_type = ctx.getChild(0).getChild(0).getSymbol().type  # it's type in terms of Parser
        if var_type == LanguageParser.BoolType:
            var_type = Visitor.BOOL
        elif var_type == LanguageParser.IntType:
            var_type = Visitor.INT
        elif var_type == LanguageParser.StringType:
            var_type = Visitor.STRING
        else:
            print("error_type: " + str(var_type))
            exit(0)
        var_name = ctx.getChild(1).getText()
        if self.current_method == 'main':
            # add field
            if var_name in self.fields:
                print("global variable " + var_name + " has been defined twice");
                exit(0)
            self.fields[var_name] = var_type
            if ctx.getChildCount() > 2:
                expr_type, expr_code = self.visitExpression(ctx.getChild(3))
                if expr_type != var_type and (expr_type not in self.PRIMITIVE or var_type not in self.PRIMITIVE):
                    print("Can't assign " + self.typeToString(expr_type) + " to the " +
                          self.typeToString(var_type) + " variable " + var_name)
                self.methods[self.current_method].code += expr_code
                self.methods[self.current_method].code.append("putstatic " + self.classname + '/' + var_name +
                                                              ' ' + self.typeToString(var_type))
        else:
            # add var
            if not self.isVisible(var_name):
                print("local variable " + var_name + " has been defined twice");
                exit(0)
            var_number = len(self.methods[self.current_method].locals)
            self.methods[self.current_method].locals.append(Visitor.Variable(var_type, var_name, var_number))
            self.visible_vars[-1][var_name] = var_number
            if ctx.getChildCount() > 2:
                expr_type, expr_code = self.visitExpression(ctx.getChild(3))
                if expr_type != var_type and (expr_type not in self.PRIMITIVE or var_type not in self.PRIMITIVE):
                    print("Can't assign " + self.typeToString(expr_type) + " to the " +
                          self.typeToString(var_type) + " variable " + var_name)
                self.methods[self.current_method].code += expr_code
                if var_type in Visitor.PRIMITIVE:
                    self.methods[self.current_method].code.append("iload " + str(var_number))
                elif var_type == Visitor.STRING:
                    self.methods[self.current_method].code.append("aload " + str(var_number))

    # everything about expressions
    def visitExpression(self, ctx: LanguageParser.ExpressionContext):
        # TODO: check children
        first_child = ctx.getChild(0)
        if hasattr(first_child, 'getRuleIndex') and first_child.getRuleIndex() == LanguageParser.RULE_assignment:
            return self.visitAssignment(first_child)

        expr_type, code = self.visitAndExpr(first_child)
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                if ctx.getChild(2 * i + 1).getText() != '||':
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitAndExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in Visitor.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = expr_type or next_expr_type
                code += next_expr_code + ['ior']
        return expr_type, code

    def visitAndExpr(self, ctx: LanguageParser.AndExprContext):
        # TODO: check children
        expr_type, code = self.visitCompExpr(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                # TODO check that child is '||'
                if ctx.getChild(2 * i + 1).getText() != '&&':
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitCompExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in Visitor.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = expr_type or next_expr_type
                code += next_expr_code + ['iand']
        return expr_type, code

    def visitCompExpr(self, ctx: LanguageParser.CompExprContext):
        # TODO: check children
        expr_type, code = self.visitArithmExpr(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('==', '!=', '>', '<', '>=', '<='):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitArithmExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in Visitor.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error


                expr_type = Visitor.BOOL
                true_label = 'Label' + self.getNextLabelNum()
                exit_label = 'Label' + self.getNextLabelNum()
                code += next_expr_code + ['if_icmp' + Visitor.OP_NAME[op] + ' ' +true_label,
                                          'iconst_0', 'goto ' + exit_label, true_label + ':',
                                          'iconst_1', exit_label + ':']
        return expr_type, code

    def visitArithmExpr(self, ctx: LanguageParser.ArithmExprContext):
        # TODO: check children
        expr_type, code = self.visitSummand(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('+', '-'):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitSummand(ctx.getChild(2 * i + 2))
                if next_expr_type not in Visitor.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = Visitor.INT
                code += next_expr_code + ['iadd' if op == '+' else 'isub']
        return expr_type, code

    def visitSummand(self, ctx: LanguageParser.SummandContext):
        # TODO: check children
        expr_type, code = self.visitMul(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('*', '/', '%'):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code = self.visitMul(ctx.getChild(2 * i + 2))
                if next_expr_type not in Visitor.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = Visitor.INT
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
            if child.getRuleIndex() == LanguageParser.RULE_var:
                return self.visitVar(child)
            elif child.getRuleIndex() == LanguageParser.RULE_funcCall:
                return self.visitFuncCall(child)
            else:
                print("error")
                exit(0)  # TODO: handle error
        else:
            if child.getSymbol().type == LanguageParser.Bool:
                return Visitor.BOOL, ['iconst_0' if child.getText() == 'false' else 'iconst_1']
            elif child.getSymbol().type == LanguageParser.Integer:
                return Visitor.INT, ['ldc ' + child.getText()]
            elif child.getSymbol().type == LanguageParser.String:
                return  Visitor.STRING, ['ldc ' + child.getText()]

 # everithing below isn't yet realized

    def visitVar(self, ctx: LanguageParser.VarContext):
        var_name = ctx.getChild(0).getText()
        if var_name in self.fields:
            var_type = self.fields[var_name]
            return var_type, ['getstatic ' + self.classname + '/' + var_name + ' ' + self.typeToString(var_type)]
        elif self.isVisible(var_name):
            var_number = self.getVarNumber(var_name)
            var_type = self.methods[self.current_method].locals[var_number].type
            if var_type in Visitor.PRIMITIVE:
                code = 'iload' + (' ' if var_number > 3 else '_') + var_number
            elif var_type == Visitor.STRING:
                code = 'aload' + (' ' if var_number > 3 else '_') + var_number
            return var_type, [code]
        else:
            print("Variable " + var_name + " is not visible")



    def visitVarType(self, ctx: LanguageParser.VarTypeContext):
        return self.typeFromParser(ctx.getChild(0).getSymbol().type)

    def visitCallArguments(self, ctx: LanguageParser.CallArgumentsContext):
        return super().visitCallArguments(ctx)

    def visitCondition(self, ctx: LanguageParser.ConditionContext):
        return super().visitCondition(ctx)

    def visitTreadCall(self, ctx: LanguageParser.TreadCallContext):
        return super().visitTreadCall(ctx)

    def visitFunctionDeclaration(self, ctx: LanguageParser.FunctionDeclarationContext):
        func_type = self.visitFuncType(ctx.getChild(0))
        func_name = ctx.getChild(1).getText()
        if func_name in self.methods:
            print("Function " + func_name + " is already defined")
        func_arguments = self.visitArguments(ctx.getChild(3))
        self.methods[func_name] = self.Method(func_type, func_arguments, None)

    def visitFunctionDefinition(self, ctx: LanguageParser.FunctionDefinitionContext):
        func_type = self.visitFuncType(ctx.getChild(0))
        func_name = ctx.getChild(1).getText()
        if func_name in self.methods:
            if self.methods[func_name].code is not None:
                print("Function " + func_name + " is already defined")
        func_arguments = self.visitArguments(ctx.getChild(3))
        if func_name in self.methods and not self.checkArguments(func_arguments, self.methods[func_name].arguments):
            print("wrong arguments for " + func_name + " function definition")
            exit(0)
        locals = self.putArgumentsToLocals(func_arguments)
        self.methods[func_name] = self.Method(func_type, func_arguments, [], locals, stack_limit=self.getStackLimitByArgs(func_arguments))
        self.current_method = func_name
        self.visitBlock(ctx.getChild(5))
        if func_type == self.VOID:
            self.methods[func_name].code.append("return")
        self.current_method = 'main'  # TODO: don't forget to fix it during the threading

    def visitFuncType(self, ctx: LanguageParser.FuncTypeContext):
        child = ctx.getChild(0)
        if hasattr(child, "getRuleIndex"):
            return self.typeFromParser(child.getChild(0).getSymbol.type)
        elif child.getSymbol().type == LanguageParser.VoidType:
            return self.VOID
        else:
            print("illegal function type: " + child.getText())
            exit(0)

    def visitArguments(self, ctx: LanguageParser.ArgumentsContext):
        arguments = []
        for i in range((ctx.getChildCount() + 1) // 2):
            arguments.append(self.visitArgument(ctx.getChild(i * 2 + 1)))
        return arguments

    def visitArgument(self, ctx: LanguageParser.ArgumentContext):
        return self.Argument(self.visitVarType(ctx.getChild(0)), ctx.getChild(1).getText())

    def visitBlock(self, ctx: LanguageParser.BlockContext):
        self.visible_vars.append({})
        for i in range(1, ctx.getChildCount() - 1):
            ctx.getChild(i).accept()
        self.visible_vars.pop()  # TODO: think about declaring new vars of the same name in the invisible for each other areas

    def visitWrite(self, ctx: LanguageParser.WriteContext):
        # TODO: check children
        expr_type, expr_code = self.visitExpression(ctx.getChild(1))
        if expr_type == Visitor.BOOL:
            expr_type = 'Z'
        elif expr_type == Visitor.INT:
            expr_type = 'I'
        elif expr_type == Visitor.STRING:
            expr_type = 'Ljava/lang/String;'
        else:
            print('error')  # TODO: handle error
            exit(0)
        return ['getstatic java/lang/System/out Ljava/io/PrintStream;'] + expr_code + \
               ['invokevirtual java/io/PrintStream/print(' + expr_type + ')V']

    def visitReturnValue(self, ctx: LanguageParser.ReturnValueContext):
        return super().visitReturnValue(ctx)

    def visitFunction(self, ctx: LanguageParser.FunctionContext):
        return super().visitFunction(ctx)

    def visitComment(self, ctx: LanguageParser.CommentContext):
        return super().visitComment(ctx)

    def visitFuncCall(self, ctx: LanguageParser.FuncCallContext):
        return super().visitFuncCall(ctx)

    def visitThread(self, ctx: LanguageParser.ThreadContext):
        return super().visitThread(ctx)

    def visitUnionDeclaration(self, ctx: LanguageParser.UnionDeclarationContext):
        return super().visitUnionDeclaration(ctx)

    def visitCycle(self, ctx: LanguageParser.CycleContext):
        return super().visitCycle(ctx)

    def visitRead(self, ctx: LanguageParser.ReadContext):
        return super().visitRead(ctx)


