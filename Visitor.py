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
                                               code =[],
                                               locals=[self.STRING])}
        self.fields = {}  # fields are stored as name: type
        self.visible_vars = [{}] # maps name: number
        self.classname = classname
        self.unions = {} # name: fields, where fields is {field_name: field type}
        self.union_length = {}

    def getNextLabelNum(self):
        self.label_num += 1
        return str(self.label_num)

    def typeLen(self, var_type):
        if var_type in self.PRIMITIVE or var_type == self.STRING:
            return 1
        else:
            return 0

    def typeToString(self, int_type):
        return 'V' if int_type == Visitor.VOID \
                else 'Z' if int_type == Visitor.BOOL \
                else 'I' if int_type == Visitor.INT  \
                else 'Ljava/lang/String;' if int_type == Visitor.STRING  \
                else '[Ljava/lang/String;' if int_type == Visitor.STRING_ARR  \
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

    def setMethodParams(self, arguments):
        local_vars = []
        visible = {}
        for arg in arguments:
            visible[arg.name] = len(local_vars)
            local_vars.append(arg.type)
        self.visible_vars.append(visible)
        self.methods[self.current_method].locals = local_vars
        self.methods[self.current_method].stack_limit = len(local_vars)  # TODO: after adding new types it will be a bit more complicated

    def buildCode(self):
        self.methods['main'].code.append("return")
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
            _, code, stack_limit = self.visitAssignment(child)
            self.methods[self.current_method].code += code[:-1]
            self.methods[self.current_method].stack_limit = max(self.methods[self.current_method].stack_limit, stack_limit)
        elif rule_index == LanguageParser.RULE_varDeclaration:
            self.visitVarDeclaration(child)
        elif rule_index == LanguageParser.RULE_funcCall:
            return_type, code, stack_limit = self.visitFuncCall(child)
            if return_type != self.VOID:
                code.append("pop")
            self.methods[self.current_method].code += code
            self.methods[self.current_method].stack_limit = max(self.methods[self.current_method].stack_limit, stack_limit)
        elif rule_index == LanguageParser.RULE_returnValue:
            self.visitReturnValue(child)
        elif rule_index == LanguageParser.RULE_condition:
            self.visitCondition(child)
        elif rule_index == LanguageParser.RULE_cycle:
            self.visitCycle(child)


    # Assignment statement that leaves the value of the variable on the top of stack
    def visitAssignment(self, ctx: LanguageParser.AssignmentContext):
        var_name = ctx.getChild(0).getText()
        if self.isVisible(var_name):
            expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(2))
            var_number = self.getVarNumber(var_name)
            var_type = self.methods[self.current_method].locals[var_number]
            if expr_type != var_type and (expr_type not in self.PRIMITIVE or var_type not in self.PRIMITIVE):
                print("Can't assign " + self.typeToString(expr_type) + " to the " +
                      self.typeToString(var_type) + " variable " + var_name)
            if var_type in Visitor.PRIMITIVE:
                expr_code.append("istore" + (' ' if var_number > 3 else '_') + str(var_number))
                expr_code.append("iload" + (' ' if var_number > 3 else '_') + str(var_number))
            elif var_type == Visitor.STRING:
                expr_code.append("astore" + (' ' if var_number > 3 else '_') + str(var_number))
                expr_code.append("aload" + (' ' if var_number > 3 else '_') + str(var_number))
            return expr_type, expr_code, stack_limit
        elif var_name in self.fields:
            expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(2))
            var_type = self.fields[var_name]
            if expr_type != var_type and (expr_type not in self.PRIMITIVE or var_type not in self.PRIMITIVE):
                print("Can't assign " + self.typeToString(expr_type) + " to the " +
                      self.typeToString(var_type) + " variable " + var_name)
            expr_code.append("putstatic " + self.classname + '/' + var_name +
                                                          ' ' + self.typeToString(var_type))
            expr_code.append("getstatic " + self.classname + '/' + var_name +
                                                          ' ' + self.typeToString(var_type))
            return expr_type, expr_code, stack_limit
        else:
            print("No such visible variable: " + var_name)
            exit(0)

    # Variable declaration (maybe with initial value)
    # If it's in the main method -- it's new field
    # Else it's local variable
    def visitVarDeclaration(self, ctx: LanguageParser.VarDeclarationContext):
        var_type = self.typeFromParser(ctx.getChild(0).getChild(0).getSymbol().type)
        if var_type is None or var_type == self.VOID:
            print("Illegal variable type " + ctx.getChild(0).getText())
            exit(0)
        var_name = ctx.getChild(1).getText()
        if self.current_method == 'main':
            # add field
            if var_name in self.fields:
                print("global variable " + var_name + " has been defined twice")
                exit(0)
            self.fields[var_name] = var_type
            if ctx.getChildCount() > 2:
                expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(3))
                if expr_type != var_type and (expr_type not in self.PRIMITIVE or var_type not in self.PRIMITIVE):
                    print("Can't assign " + self.typeToString(expr_type) + " to the " +
                          self.typeToString(var_type) + " variable " + var_name)
                self.methods[self.current_method].code += expr_code
                self.methods[self.current_method].code.append("putstatic " + self.classname + '/' + var_name +
                                                              ' ' + self.typeToString(var_type))
                self.methods[self.current_method].stack_limit = max(self.methods[self.current_method].stack_limit, stack_limit)
        else:
            # add var
            if self.isVisible(var_name):
                print("local variable " + var_name + " has been defined twice")
                exit(0)
            var_number = len(self.methods[self.current_method].locals)
            self.methods[self.current_method].locals.append(var_type)
            self.visible_vars[-1][var_name] = var_number
            if ctx.getChildCount() > 2:
                expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(3))
                if expr_type != var_type and (expr_type not in self.PRIMITIVE or var_type not in self.PRIMITIVE):
                    print("Can't assign " + self.typeToString(expr_type) + " to the " +
                          self.typeToString(var_type) + " variable " + var_name)
                self.methods[self.current_method].code += expr_code
                if var_type in Visitor.PRIMITIVE:
                    self.methods[self.current_method].code.append("istore" + (' ' if var_number > 3 else '_') + str(var_number))
                elif var_type == Visitor.STRING:
                    self.methods[self.current_method].code.append("astore" + (' ' if var_number > 3 else '_') + str(var_number))
                self.methods[self.current_method].stack_limit = max(self.methods[self.current_method].stack_limit, stack_limit + 1)


    # everything about expressions
    def visitExpression(self, ctx: LanguageParser.ExpressionContext):
        # TODO: check children
        first_child = ctx.getChild(0)
        if hasattr(first_child, 'getRuleIndex') and first_child.getRuleIndex() == LanguageParser.RULE_assignment:
            return self.visitAssignment(first_child)

        expr_type, code, stack_limit = self.visitAndExpr(first_child)
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                if ctx.getChild(2 * i + 1).getText() != '||':
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code, next_stack_limit = self.visitAndExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in Visitor.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = expr_type or next_expr_type
                code += next_expr_code + ['ior']
                stack_limit = max(stack_limit, next_stack_limit)
        return expr_type, code, stack_limit

    def visitAndExpr(self, ctx: LanguageParser.AndExprContext):
        # TODO: check children
        expr_type, code, stack_limit = self.visitCompExpr(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                # TODO check that child is '||'
                if ctx.getChild(2 * i + 1).getText() != '&&':
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code, next_stack_limit = self.visitCompExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in Visitor.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = expr_type or next_expr_type
                code += next_expr_code + ['iand']
                stack_limit = max(stack_limit, next_stack_limit + 1)
        return expr_type, code, stack_limit

    def visitCompExpr(self, ctx: LanguageParser.CompExprContext):
        # TODO: check children
        expr_type, code, stack_limit = self.visitArithmExpr(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('==', '!=', '>', '<', '>=', '<='):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code, next_stack_limit = self.visitArithmExpr(ctx.getChild(2 * i + 2))
                if next_expr_type not in Visitor.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error


                expr_type = Visitor.BOOL
                true_label = 'Label' + self.getNextLabelNum()
                exit_label = 'Label' + self.getNextLabelNum()
                code += next_expr_code + ['if_icmp' + Visitor.OP_NAME[op] + ' ' +true_label,
                                          'iconst_0', 'goto ' + exit_label, true_label + ':',
                                          'iconst_1', exit_label + ':']
                stack_limit = max(stack_limit, next_stack_limit + 1)
        return expr_type, code, stack_limit

    def visitArithmExpr(self, ctx: LanguageParser.ArithmExprContext):
        # TODO: check children
        expr_type, code, stack_limit = self.visitSummand(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('+', '-'):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code, next_stack_limit = self.visitSummand(ctx.getChild(2 * i + 2))
                if next_expr_type not in Visitor.PRIMITIVE:
                    print("error")
                    exit(0)  # TODO handle error

                expr_type = Visitor.INT
                code += next_expr_code + ['iadd' if op == '+' else 'isub']
                stack_limit = max(stack_limit, next_stack_limit + 1)
        return expr_type, code, stack_limit

    def visitSummand(self, ctx: LanguageParser.SummandContext):
        # TODO: check children
        expr_type, code, stack_limit = self.visitMul(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type not in Visitor.PRIMITIVE or ctx.getChildCount() % 2 == 0:
                print("error")
                exit(0)  # TODO handle error

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('*', '/', '%'):
                    print("error")
                    exit(0)  # TODO handle error

                next_expr_type, next_expr_code, next_stack_limit = self.visitMul(ctx.getChild(2 * i + 2))
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
                stack_limit = max(stack_limit, next_stack_limit + 1)
        return expr_type, code, stack_limit

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
                return Visitor.BOOL, ['iconst_0' if child.getText() == 'false' else 'iconst_1'], 1
            elif child.getSymbol().type == LanguageParser.Integer:
                return Visitor.INT, ['ldc ' + child.getText()], 1
            elif child.getSymbol().type == LanguageParser.String:
                return  Visitor.STRING, ['ldc ' + child.getText()], 1

    def visitVar(self, ctx: LanguageParser.VarContext):
        var_name = ctx.getChild(0).getText()
        if self.isVisible(var_name):
            var_number = self.getVarNumber(var_name)
            var_type = self.methods[self.current_method].locals[var_number]
            if var_type in Visitor.PRIMITIVE:
                code = 'iload' + (' ' if var_number > 3 else '_') + str(var_number)
            elif var_type == Visitor.STRING:
                code = 'aload' + (' ' if var_number > 3 else '_') + str(var_number)
            else:
                print("Wrong variable type")
                exit(0)
            return var_type, [code], 1  # TODO: depends on variable type
        elif var_name in self.fields:
            var_type = self.fields[var_name]
            return var_type, ['getstatic ' + self.classname + '/' + var_name + ' ' + self.typeToString(var_type)], 1  # TODO: depends on variable type
        else:
            print("Variable " + var_name + " is not visible")
            exit(0)

    def visitFuncCall(self, ctx: LanguageParser.FuncCallContext):
        func_name = ctx.getChild(0).getText()
        arg_types, arg_codes, stack_limit = self.visitCallArguments(ctx.getChild(2))
        if func_name not in self.methods:
            print("Undefined function: " + func_name)
            exit(0)
        method = self.methods[func_name]

        if len(arg_types) != len(method.arguments):
            print("Wrong number of argumentsfor " + func_name + ". " + str(len(arg_types)) +" instead of " + str(len(method.arguments)))
            exit(0)
        for i in range(len(arg_types)):
            if arg_types[i] != method.arguments[i].type:
                # hope that there are no functions with more than 20 arguments
                print("Wrong " + str(i + 1) + ('st' if i == 0 else 'nd' if i == 1 else 'th') + " argument type for " + func_name + ".")
                exit(0)
        if method.return_type != self.VOID:
            stack_limit = max(stack_limit, 1)  # if there no arguments, but we need place to put return value
        code = []
        for arg_code in arg_codes:
            code += arg_code
        code.append("invokestatic " + self.classname + '/' + func_name + '(' + "".join([self.typeToString(i) for i in arg_types]) + ')' + self.typeToString(method.return_type))
        return method.return_type, code, stack_limit

    def visitCallArguments(self, ctx: LanguageParser.CallArgumentsContext):
        types, expressions = [], []
        stack_limit = 0
        for i in range((ctx.getChildCount() + 1) // 2):
            expr_type, expr_code, expr_stack_limit = self.visitExpression(ctx.getChild(2 * i))
            types.append(expr_type)
            expressions.append(expr_code)
            stack_limit = max(stack_limit, expr_stack_limit + i)
        return types, expressions, stack_limit

    def visitVarType(self, ctx: LanguageParser.VarTypeContext):
        return self.typeFromParser(ctx.getChild(0).getSymbol().type)



    def visitCondition(self, ctx: LanguageParser.ConditionContext):
        expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(1))  # TODO: check type
        cur_method = self.methods[self.current_method]
        cur_method.stack_limit = max(cur_method.stack_limit, stack_limit)
        false_label = "Label" + str(self.getNextLabelNum())
        cur_method.code += expr_code
        cur_method.code.append("ifeq " + false_label)
        self.visitBlock(ctx.getChild(2))
        if ctx.getChildCount() > 3:
            exit_label = "Label" + str(self.getNextLabelNum())
            cur_method.code.append("goto " + exit_label)
            cur_method.code.append(false_label + ":")
            self.visitBlock(ctx.getChild(4))
            cur_method.code.append(exit_label + ":")
        else:
            cur_method.code.append(false_label + ":")


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
        self.methods[func_name] = self.Method(func_type, func_arguments, [])
        self.current_method = func_name
        self.setMethodParams(func_arguments)

        self.visitBlock(ctx.getChild(5))
        if func_type == self.VOID:
            self.methods[func_name].code.append("return")

        self.visible_vars.pop()
        self.current_method = 'main'

    def visitFuncType(self, ctx: LanguageParser.FuncTypeContext):
        child = ctx.getChild(0)
        if hasattr(child, "getRuleIndex"):
            return self.typeFromParser(child.getChild(0).getSymbol().type)
        elif child.getSymbol().type == LanguageParser.VoidType:
            return self.VOID
        else:
            print("illegal function type: " + child.getText())
            exit(0)

    def visitArguments(self, ctx: LanguageParser.ArgumentsContext):
        arguments = []
        for i in range((ctx.getChildCount() + 1) // 2):
            arguments.append(self.visitArgument(ctx.getChild(i * 2)))
        return arguments

    def visitArgument(self, ctx: LanguageParser.ArgumentContext):
        return self.Argument(self.visitVarType(ctx.getChild(0)), ctx.getChild(1).getText())

    def visitBlock(self, ctx: LanguageParser.BlockContext):
        self.visible_vars.append({})
        for i in range(1, ctx.getChildCount() - 1):
            ctx.getChild(i).accept(self)
        self.visible_vars.pop()

    def visitWrite(self, ctx: LanguageParser.WriteContext):
        # TODO: check children
        expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(1))
        if expr_type == Visitor.BOOL:
            expr_type = 'Z'
        elif expr_type == Visitor.INT:
            expr_type = 'I'
        elif expr_type == Visitor.STRING:
            expr_type = 'Ljava/lang/String;'
        else:
            print('error')  # TODO: handle error
            exit(0)
        self.methods[self.current_method].stack_limit = max(self.methods[self.current_method].stack_limit, stack_limit + 1)
        return ['getstatic java/lang/System/out Ljava/io/PrintStream;'] + expr_code + \
               ['invokevirtual java/io/PrintStream/print(' + expr_type + ')V']

    def visitReturnValue(self, ctx: LanguageParser.ReturnValueContext):
        ret_type = self.methods[self.current_method].return_type
        if ctx.getChildCount() == 1:
            if self.methods[self.current_method].return_type != self.VOID:
                print("Function " + self.current_method + " can not return void value")
                exit(0)
            self.methods[self.current_method].code.append("return")
        else:
            expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(1))
            if ret_type != expr_type and (ret_type not in self.PRIMITIVE or expr_type not in self.PRIMITIVE):
                print("Wrong return type for function " + self.current_method)
                exit(0)
            self.methods[self.current_method].stack_limit = max(self.methods[self.current_method].stack_limit, stack_limit)
            expr_code.append("ireturn" if ret_type in self.PRIMITIVE else "areturn" if ret_type == self.STRING else None)
            self.methods[self.current_method].code += expr_code



    def visitFunction(self, ctx: LanguageParser.FunctionContext):
        return super().visitFunction(ctx)

    def visitComment(self, ctx: LanguageParser.CommentContext):
        return super().visitComment(ctx)



    def visitThread(self, ctx: LanguageParser.ThreadContext):
        return super().visitThread(ctx)

    def visitUnionDeclaration(self, ctx: LanguageParser.UnionDeclarationContext):
        name = ctx.getChild(1).getText()
        if name in self.unions:
            print("Union " + name + " hsa already been declared")
            exit(0)
        fields = {}
        union_size = 1
        for i in range(3, ctx.getChildCount() - 1):
            field_type, field_name = self.visitUnionField(ctx.getChild(i))
            if field_name in fields:
                print("Union " + name + " has more then one field " + field_name)
                exit(0)
            if field_type == self.VOID:
                print("Union " + name + " contains void field")
                exit(0)
            if field_type not in self.PRIMITIVE and field_type != self.STRING:
                union_size = 2
            fields[field_name] = field_type
        self.unions[name] = fields
        method_locals = self.methods[self.current_method].locals
        self.visible_vars[-1][name] = len(method_locals)
        method_locals += [self.UNION] * union_size

    def visitUnionField(self, ctx: LanguageParser.UnionFieldContext):
        return self.typeFromParser(ctx.getChild(0).getSymbol().type), ctx.getChild(1).getText()

    def visitCycle(self, ctx: LanguageParser.CycleContext):
        expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(1))  # TODO: check type
        cur_method = self.methods[self.current_method]
        cur_method.stack_limit = max(cur_method.stack_limit, stack_limit)
        start_label = "Label" + str(self.getNextLabelNum())
        exit_label = "Label" + str(self.getNextLabelNum())
        cur_method.code.append(start_label + ":")
        cur_method.code += expr_code
        cur_method.code.append("ifeq " + exit_label)
        self.visitBlock(ctx.getChild(2))
        cur_method.code.append("goto " + start_label)
        cur_method.code.append(exit_label + ":")

    def visitRead(self, ctx: LanguageParser.ReadContext):
        return super().visitRead(ctx)


