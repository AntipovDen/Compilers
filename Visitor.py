from gen.LanguageVisitor import LanguageVisitor
from gen.LanguageParser import LanguageParser


# Constants
BOOL = 0
INT = 1
STRING = 2
UNION = 3
VOID = 4
STRING_ARR = 5
LONG = 6
FLOAT = 7
DOUBLE = 8
PRIMITIVE = (0, 1)
LONG_TYPES = (8, 6)
THREAD = 9
OP_NAME = {'==': 'eq', '!=': 'ne', '>': 'gt', '<': 'lt', '>=': 'ge', '<=': 'le'}
TYPE_DESCRIPTOR = {BOOL: 'Z', INT: 'I', STRING: 'Ljava/lang/String;', STRING_ARR: '[Ljava/lang/String;',
                   LONG: 'J', FLOAT: 'F', DOUBLE: 'D', VOID: 'V'}
TYPE_LETTER = {BOOL: 'i', INT: 'i', LONG: 'l', FLOAT: 'f', DOUBLE: 'd', STRING: 'a'}
PARSER_TYPE = {LanguageParser.VoidType: VOID, LanguageParser.BoolType: BOOL, LanguageParser.IntType: INT,
               LanguageParser.LongType: LONG, LanguageParser.FloatType: FLOAT, LanguageParser.DoubleType: DOUBLE,
               LanguageParser.StringType: STRING}
CONST_TYPE = {LanguageParser.String: STRING, LanguageParser.Bool: BOOL, LanguageParser.Integer: INT,
              LanguageParser.Long: LONG, LanguageParser.Float: FLOAT, LanguageParser.Double: DOUBLE}

label_num = -1


class Method:
    def __init__(self, return_type=-1, arguments=None, code=CodeNode(), local_constants=None, stack_limit=0):
        self.return_type = return_type
        self.arguments = arguments if arguments is not None else []
        self.code = code
        self.locals = local_constants if local_constants is not None else []
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


class CodeNode:
    def __init__(self, *args, **kwargs):
        self.code = list(args)
        if 'children' in kwargs:
            self.children = kwargs['children']
        else:
            self.children = []

    def build_code(self):
        code = []
        for c in self.children:
            code += c.build_code()
        return code + self.code


def type_len(var_type):
    if var_type in (BOOL, INT, STRING, FLOAT):
        return 1
    elif var_type in LONG_TYPES:
        return 2
    else:
        print("Unknown type number " + str(var_type))
        exit(0)


def type_to_string(input_type):
    if input_type in TYPE_DESCRIPTOR:
        return TYPE_DESCRIPTOR[input_type]
    return None


def type_from_parser(parser_type):
    if parser_type in PARSER_TYPE:
        return PARSER_TYPE[parser_type]
    return None


def const_type_from_parser(parser_type):
    if parser_type in CONST_TYPE:
        return CONST_TYPE[parser_type]
    return None


def check_arguments(arguments1, arguments2):
    if len(arguments1) != len(arguments2):
        return False
    for i in range(len(arguments1)):
        if arguments1[i] != arguments2[i]:
            return False
    return True


def common_cast_type(type1, type2):
    if type1 == type2:
        return type1
    if type1 == FLOAT or type2 == FLOAT:
        return DOUBLE
    if type1 == STRING or type2 == STRING and type1 != type2:
        return None
    return max(type1, type2)  # suppose that constants are in following order: BOOL < INT < LONG < DOUBLE


def letter(type_num):
    if type_num in TYPE_LETTER:
        return TYPE_LETTER[type_num]
    return None


def cast(type_from, type_to):
    return letter(type_from) + '2' + letter(type_to)


def get_next_label_num():
    global label_num
    label_num += 1
    return str(label_num)


def int_to_bool():
    exit_label = 'Label' + str(get_next_label_num())
    return ['dup', 'ifeq ' + exit_label, 'pop', 'iconst_1', exit_label + ':']


class Visitor(LanguageVisitor):
              
    def __init__(self, classname, main_class=None):
        self.label_num = -1
        self.local_variable_num = -1
        # WARNING! it's made in this way because of only threads are needed.
        # Actually it must be easy to make classes here
        self.current_method = Method(return_type=VOID,
                                     arguments=[Argument(arg_type=STRING_ARR, name='args')],
                                     code=CodeNode(),
                                     local_constants=[STRING]) if main_class is None else \
                              Method(return_type=VOID,
                                     arguments=[],
                                     code=CodeNode,
                                     local_constants=[THREAD])
        self.methods = {'main' if main_class is None else 'run': self.current_method}
        self.fields = {}  # fields are stored as name: type
        self.visible_vars = [{}]  # maps name: number
        self.classname = classname  # the name of the visitor's class
        self.unions = {}  # name: fields, where fields is {field_name: field type}
        self.union_length = {}  # name: length
        self.has_reader = False  # if we need to keep scanner field in this class. Only possible for main class
        self.main_class = main_class  # if we are in the main class or in the thread
        self.threads = {}  # tread_name: thread code

    def is_visible(self, var_name):
        for vis in self.visible_vars:
            if var_name in vis:
                return True
        return False

    def get_var_number(self, var_name):
        for vis in self.visible_vars:
            if var_name in vis:
                return vis[var_name]
        return None

    def set_method_params(self, arguments):
        if self.main_class is None:
            local_vars = []
        else:
            local_vars = [THREAD]
        visible = {}
        for arg in arguments:
            visible[arg.name] = len(local_vars)
            local_vars.append(arg.type)
            if arg.type in LONG_TYPES:
                local_vars.append(arg.type)
        self.visible_vars.append(visible)
        self.current_method.locals = local_vars
        self.current_method.stack_limit = 0

    def build_code(self):
        self.methods['main'].code.append("return")
        code = list()
        code.append(".class " + self.classname)
        code.append(".super java/lang/Object")
        code.append("")
        for field in self.fields:
            code.append(".field public static volatile " + field + ' ' + type_to_string(self.fields[field]))
        if self.has_reader:
            code.append(".field public static Sc Ljava/util/Scanner;")
            main = self.methods['main']
            main.code = ['new java/util/Scanner',
                         'dup',
                         'getstatic java/lang/System in Ljava/io/InputStream;',
                         'invokespecial java/util/Scanner/<init>(Ljava/io/InputStream;)V',
                         'putstatic ' + self.classname + ' Sc Ljava/util/Scanner;'] + main.code
            main.stack_limit = max(main.stack_limit, 3)

        code.append("")
        for method in self.methods:
            method_params = self.methods[method]
            method_type = type_to_string(method_params.return_type)
            args = ""
            for arg in method_params.arguments:
                args += type_to_string(arg.type)
            code.append(".method public static " + method + " : (" + args + ")" + method_type)
            code.append(".limit stack " + str(method_params.stack_limit))
            code.append(".limit locals " + str(len(method_params.locals) + len(method_params.arguments)))
            code += method_params.code.build_code()
            code.append(".end method")
            code.append("")
        code.append(".end class")

        code.append("")
        for t in self.threads:
            code += self.threads[t]
            code.append("")
        return code

    def build_thread_code(self):
        code = list()
        code.append(".class " + self.classname)
        code.append(".super java/lang/Object")
        code.append(".implements java/lang/Runnable")
        code.append("")
        for field in self.fields:
            code.append(".field public " + field + ' ' + type_to_string(self.fields[field]))
        code.append("")
        code.append(".method public <init> : ()V")
        code.append(".limit stack 1")
        code.append(".limit locals 1")
        code.append("    aload_0")
        code.append("    invokespecial java/lang/Object/<init>()V")
        code.append("    return")
        code.append(".end method")
        code.append("")
        for method in self.methods:
            method_params = self.methods[method]
            method_type = type_to_string(method_params.return_type)
            args = ""
            for arg in method_params.arguments:
                args += type_to_string(arg.type)
            code.append(".method public " + method + " : (" + args + ")" + method_type)
            code.append(".limit stack " + str(method_params.stack_limit))
            code.append(".limit locals " + str(len(method_params.locals) + len(method_params.arguments)))
            code += method_params.code.build_code()
            code.append(".end method")
            code.append("")
        code.append(".end class")
        return code

    def visitProgram(self, ctx: LanguageParser.ProgramContext):
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if not hasattr(child, 'getRuleIndex'):
                print("Unexpected terminal token in program")
                exit(0)
            if child.getRuleIndex() != LanguageParser.RULE_comment:
                child.accept(self)

    def visitCommand(self, ctx: LanguageParser.CommandContext):
        child = ctx.getChild(0)
        rule_index = child.getRuleIndex()
        method = self.current_method
        if rule_index == LanguageParser.RULE_write:
            method.code.children.append(self.visitWrite(child))
        elif rule_index == LanguageParser.RULE_assignment:
            var_type, code, stack_limit = self.visitAssignment(child)
            code.code.append("pop" + ("2" if var_type in LONG_TYPES else ""))
            method.code.children.append(code)
            method.stack_limit = max(method.stack_limit, stack_limit)
        # from here codeNodes are not implemented
        elif rule_index == LanguageParser.RULE_varDeclaration:
            self.visitVarDeclaration(child)
        elif rule_index == LanguageParser.RULE_funcCall:
            return_type, code, stack_limit = self.visitFuncCall(child)
            if return_type != VOID:
                code.append("pop")
            method.code += code
            method.stack_limit = max(method.stack_limit, stack_limit)
        elif rule_index == LanguageParser.RULE_returnValue:
            self.visitReturnValue(child)
        elif rule_index == LanguageParser.RULE_condition:
            self.visitCondition(child)
        elif rule_index == LanguageParser.RULE_cycle:
            self.visitCycle(child)
        elif rule_index == LanguageParser.RULE_unionDeclaration:
            self.visitUnionDeclaration(child)
        elif rule_index == LanguageParser.RULE_read:
            self.visitRead(child)
        elif rule_index == LanguageParser.RULE_treadCall:
            self.visitTreadCall(child)
        elif rule_index == LanguageParser.RULE_getLock:
            self.visitGetLock(child)
        elif rule_index == LanguageParser.RULE_releaseLock:
            self.visitReleaseLock(child)
        else:
            print("Wrong command")
            exit(0)

    # Assignment statement that leaves the value of the variable on the top of stack
    def visitAssignment(self, ctx: LanguageParser.AssignmentContext):
        var_name = ctx.getChild(0).getText()

        if ctx.getChildCount() > 3:
            var_field = ctx.getChild(2).getText()
            expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(4))
        else:
            var_field = None
            expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(2))

        if self.is_visible(var_name):
            var_number = self.get_var_number(var_name)
            var_type = self.current_method.locals[var_number]
            if var_type == UNION:
                if var_field is None:
                    print("You should specify the field of union " + var_name)
                    exit(0)
                if var_field in self.unions[var_name]:
                    var_type = self.unions[var_name][var_field]
                else:
                    print("Wrong field name for union " + var_name + ": " + var_field)
                    exit(0)
            else:
                if var_field is not None:
                    print("Only unions can have fields, not variable " + var_name)

            if var_type != common_cast_type(expr_type, var_type):
                print("Can't assign " + type_to_string(expr_type) + " to the " +
                      type_to_string(var_type) + " variable " + var_name)

            code = CodeNode("dup" + ("2" if var_type in LONG_TYPES else ""),
                            letter(var_type) + "store" + (' ' if var_number > 3 else '_') + str(var_number),
                            children=[expr_code])
            if var_type != expr_type:
                code.children.append(CodeNode(cast(expr_type, var_type)))
            return expr_type, expr_code, max(stack_limit, 2 * type_len(var_type))
        elif var_name in self.fields or self.main_class is not None and var_name in self.main_class.fields:
            if var_field is not None:
                print("Global variables like " + var_name + " can't be unions, so they can't have fields")
                exit(0)
            if var_name in self.fields:
                var_type = self.fields[var_name]
                classname = self.classname
            else:
                var_type = self.main_class.fields[var_name]
                classname = self.main_class.classname

            if var_type != common_cast_type(expr_type, var_type):
                print("Can't assign " + type_to_string(expr_type) + " to the " +
                      type_to_string(var_type) + " variable " + var_name)


            if var_name in self.fields and self.main_class is not None:
                code = CodeNode("putfield " + classname + ' ' + var_name + ' ' + type_to_string(var_type),
                                "getfield " + classname + ' ' + var_name + ' ' + type_to_string(var_type),
                                children=[CodeNode("aload_0"), expr_code])
                stack_limit += 1
            else:
                code = CodeNode("putstatic " + classname + ' ' + var_name + ' ' + type_to_string(var_type),
                                "getstatic " + classname + ' ' + var_name + ' ' + type_to_string(var_type),
                                children=[expr_code])

            if var_type != expr_type:
                code.children.append(CodeNode(cast(expr_type, var_type)))
            return expr_type, expr_code, stack_limit
        else:
            print("No such visible variable: " + var_name)
            exit(0)

    # Variable declaration (maybe with initial value)
    # If it's in the main method -- it's new field
    # Else it's local variable
    def visitVarDeclaration(self, ctx: LanguageParser.VarDeclarationContext):
        var_type = self.visitVarType(ctx.getChild(0))
        if var_type is None or var_type == VOID:
            print("Illegal variable type " + ctx.getChild(0).getText())
            exit(0)
        var_name = ctx.getChild(1).getText()
        if self.main_class is None and self.current_method == self.methods['main'] or \
           self.main_class is not None and self.current_method == self.methods['run']:
            # add field
            if var_name in self.fields:
                print("global variable " + var_name + " has been defined twice")
                exit(0)
            self.fields[var_name] = var_type
            if ctx.getChildCount() > 2:
                expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(3))
                if common_cast_type(expr_type, var_type) != var_type:
                    print("Can't assign " + type_to_string(expr_type) + " to the " +
                          type_to_string(var_type) + " variable " + var_name + ". Use explicit cast.")
                method = self.current_method
                if self.main_class is not None:
                    method.code.append("aload_0")
                    stack_limit += 1
                method.code += expr_code
                if expr_type < var_type:
                    method.code.append(letter(expr_type) + '2' + letter(var_type))
                if self.main_class is None:
                    method.code.append("putstatic " + self.classname + '/' + var_name +
                                       ' ' + type_to_string(var_type))
                else:
                    method.code.append("putfield " + self.classname + '/' + var_name +
                                       ' ' + type_to_string(var_type))
                method.stack_limit = max(method.stack_limit, stack_limit, type_len(var_type))
        else:
            # add var
            if self.is_visible(var_name):
                print("local variable " + var_name + " has been defined twice")
                exit(0)
            method = self.current_method
            var_number = len(method.locals)
            method.locals += [var_type] * type_len(var_type)
            self.visible_vars[-1][var_name] = var_number
            if ctx.getChildCount() > 2:
                expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(3))
                if common_cast_type(expr_type, var_type) != var_type:
                    print("Can't assign " + type_to_string(expr_type) + " to the " +
                          type_to_string(var_type) + " variable " + var_name + ". Use explicit cast.")
                method.code += expr_code
                if expr_type < var_type:
                    method.code.append(letter(expr_type) + '2' + letter(var_type))
                method.code.append(letter(var_type) + "store" + (' ' if var_number > 3 else '_') + str(var_number))
                method.stack_limit = max(method.stack_limit, stack_limit, type_len(var_type))

    # everything about expressions
    def visitExpression(self, ctx: LanguageParser.ExpressionContext):
        first_child = ctx.getChild(0)
        if hasattr(first_child, 'getRuleIndex') and first_child.getRuleIndex() == LanguageParser.RULE_assignment:
            return self.visitAssignment(first_child)

        expr_type, code, stack_limit = self.visitAndExpr(first_child)
        if ctx.getChildCount() > 1:
            if expr_type == STRING:
                print("Please, don't ask me to or two strings, I can't do that")
                exit(0)

            code = CodeNode(children=[code])

            next_label = "Label" + str(get_next_label_num())

            for i in range((ctx.getChildCount() - 1) // 2):
                if expr_type == INT:
                    jump_code = int_to_bool()
                elif expr_type == FLOAT:
                    jump_code = ['fconst_0', 'fcmpg']
                elif expr_type == DOUBLE:
                    jump_code = ['dconst_0', 'dcmpg']
                elif expr_type == LONG:
                    jump_code = ['lconst_0', 'lcmp']
                else:
                    jump_code = []
                jump_code.append("dup")
                jump_code.append("ifne " + next_label)
                jump_code.append("pop")
                code.children.append(CodeNode(*jump_code))
                stack_limit = max(stack_limit, type_len(expr_type) * 2)

                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('||', 'V'):
                    print("Unknown operation: " + op)
                    exit(0)

                next_expr_type, next_expr_code, next_stack_limit = self.visitAndExpr(ctx.getChild(2 * i + 2))

                if next_expr_type not in (BOOL, INT, LONG, DOUBLE, FLOAT):
                    print("Wrong operand type for " + op + " operation")
                    exit(0)

                code.children.append(next_expr_code)

                stack_limit = max(stack_limit, next_stack_limit)
                if op == 'V':
                    if next_expr_type == INT:
                        add_code = int_to_bool()
                    elif next_expr_type == FLOAT:
                        add_code = ['fconst_0', 'fcmpg', 'dup', 'imul']
                    elif next_expr_type == DOUBLE:
                        add_code = ['dconst_0', 'dcmpg', 'dup2', 'imul']
                    elif next_expr_type == LONG:
                        add_code = ['lconst_0', 'lcmp', 'dup2', 'imul']
                    else:
                        add_code = []
                    add_code += [next_label + ':', 'ineg', 'iconst_1', 'iadd']
                    code.children.append(CodeNode(*add_code))
                    next_label = 'Label' + str(get_next_label_num())
                    stack_limit = max(stack_limit, type_len(next_expr_type) * 2)
                expr_type = BOOL
            code.code = [next_label + ':']
        return expr_type, code, stack_limit

    def visitAndExpr(self, ctx: LanguageParser.AndExprContext):
        expr_type, code, stack_limit = self.visitCompExpr(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type == STRING:
                print("Please, don't ask me to and two strings, I can't do that")
                exit(0)

            next_label = 'Label' + str(get_next_label_num())
            code = CodeNode(children=[code])

            for i in range((ctx.getChildCount() - 1) // 2):
                if expr_type == INT:
                    jump_code = int_to_bool()
                elif expr_type == FLOAT:
                    jump_code = ['fconst_0', 'fcmpg']
                elif expr_type == DOUBLE:
                    jump_code = ['dconst_0', 'dcmpg']
                elif expr_type == LONG:
                    jump_code = ['lconst_0', 'lcmp']
                else:
                    jump_code = []
                jump_code.append("dup")
                jump_code.append("ifeq " + next_label)
                jump_code.append("pop")
                code.children.append(CodeNode(*jump_code))
                stack_limit = max(stack_limit, type_len(expr_type) * 2)

                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('&&', '|'):
                    print("Unknown operation " + op)
                    exit(0)

                next_expr_type, next_expr_code, next_stack_limit = self.visitCompExpr(ctx.getChild(2 * i + 2))

                if next_expr_type not in (BOOL, INT, LONG, DOUBLE, FLOAT):
                    print("Wrong operand type for " + op + " operation")
                    exit(0)

                code.children.append(next_expr_code)

                stack_limit = max(stack_limit, next_stack_limit)
                if op == '|':
                    if next_expr_type == INT:
                        add_code = int_to_bool()
                    elif next_expr_type == FLOAT:
                        add_code = ['fconst_0', 'fcmpg', 'dup', 'imul']
                    elif next_expr_type == DOUBLE:
                        add_code = ['dconst_0', 'dcmpg', 'dup2', 'imul']
                    elif next_expr_type == LONG:
                        add_code = ['lconst_0', 'lcmp', 'dup2', 'imul']
                    else:
                        add_code = []
                    add_code += [next_label + ':', 'ineg', 'iconst_1', 'iadd']
                    code.children.append(CodeNode(*add_code))
                    next_label = 'Label' + str(get_next_label_num())
                    stack_limit = max(stack_limit, type_len(next_expr_type) * 2)
                expr_type = BOOL
            code.code = [next_label + ':']
        return expr_type, code, stack_limit

    def visitCompExpr(self, ctx: LanguageParser.CompExprContext):
        neg = not hasattr(ctx.getChild(0), 'getRuleIndex') and ctx.getChild(0).getText() == '!'
        expr_type, code, stack_limit = self.visitArithmExpr(ctx.getChild(neg))
        if ctx.getChildCount() > (1 + neg):
            if expr_type == STRING:
                print("Please, don't ask me to compare strings, I can't do that:(")
                exit(0)

            code = CodeNode(children=[code])

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1 + neg).getText()
                if op not in OP_NAME:
                    print("Unknown operation")
                    exit(0)

                next_expr_type, next_expr_code, next_stack_limit = self.visitArithmExpr(ctx.getChild(2 * i + 2 + neg))

                if next_expr_type not in (BOOL, INT, LONG, DOUBLE, FLOAT):
                    print("Wrong operand type for " + op + " operation")
                    exit(0)

                common_type = common_cast_type(expr_type, next_expr_type)
                if common_type > expr_type and common_type != INT:
                    code.children.append(CodeNode(cast(expr_type, common_type)))

                code.children.append(next_expr_code)
                if common_type > next_expr_type and common_type != INT:
                    code.children.append(CodeNode(cast(next_expr_type, common_type)))
                    next_stack_limit = max(next_stack_limit, 2)

                expr_type = BOOL
                true_label = 'Label' + get_next_label_num()
                exit_label = 'Label' + get_next_label_num()
                if common_type in (LONG, DOUBLE, FLOAT):
                    code.children.append(CodeNode(letter(common_type) + "cmp" + ('g' if common_type != LONG else ''),
                                                  'if' + OP_NAME[op] + ' ' + true_label,
                                                  'iconst_0', 'goto ' + exit_label, true_label + ':',
                                                  'iconst_1', exit_label + ':'))
                else:
                    code.children.append(CodeNode('if_icmp' + OP_NAME[op] + ' ' + true_label,
                                                  'iconst_0', 'goto ' + exit_label, true_label + ':',
                                                  'iconst_1', exit_label + ':'))
                stack_limit = max(stack_limit, next_stack_limit + type_len(common_type))
        if neg:
            if expr_type == BOOL:
                code = CodeNode('ineg', 'iconst_1', 'iadd', children = [code])
                stack_limit = max(stack_limit, 2)
            elif expr_type == INT:
                true_label = 'Label' + str(get_next_label_num())
                exit_label = 'Label' + str(get_next_label_num())
                code = CodeNode('ifeq ' + true_label, 'iconst_0', 'goto ' + exit_label,
                                true_label + ':', 'iconst_1', exit_label + ':', children=[code])
                expr_type = BOOL
            else:
                code = CodeNode(letter(expr_type) + 'const_0',
                       letter(expr_type) + 'cmp' + ('g' if expr_type != LONG else ''),
                       'dup', 'imul', 'ineg', 'iconst_1', 'iadd', children=[code])
                stack_limit = max(stack_limit, 2 * type_len(expr_type))
                expr_type = BOOL

        return expr_type, code, stack_limit

    def visitArithmExpr(self, ctx: LanguageParser.ArithmExprContext):
        expr_type, code, stack_limit = self.visitSummand(ctx.getChild(0))
        if ctx.getChildCount() > 1:
            if expr_type == STRING:
                print("Can't perfom operations with strings")
                exit(0)
            code = CodeNode(children=[code])

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('+', '-'):
                    print("Unknown operation: " + op)
                    exit(0)

                next_expr_type, next_expr_code, next_stack_limit = self.visitSummand(ctx.getChild(2 * i + 2))

                if next_expr_type not in (BOOL, INT, LONG, DOUBLE, FLOAT):
                    print("Wrong operand type for " + op + " operation")
                    exit(0)

                common_type = common_cast_type(expr_type, next_expr_type)
                if common_type > expr_type and common_type != INT:
                    code.children.append(CodeNode(cast(expr_type, common_type)))
                code.children.append(next_expr_code)
                if common_type > next_expr_type and common_type != INT:
                    code.children.append(CodeNode(cast(next_expr_type, common_type)))
                    next_stack_limit = max(next_stack_limit, 2)
                code.children.append(CodeNode(letter(common_type) + ('add' if op == '+' else 'sub')))
                stack_limit = max(stack_limit, next_stack_limit + type_len(next_expr_type))
                expr_type = common_type
        return expr_type, code, stack_limit

    def visitSummand(self, ctx: LanguageParser.SummandContext):
        expr_type, code, stack_limit = ctx.getChild(0).accept(self)
        if ctx.getChildCount() > 1:
            if expr_type == STRING:
                print("Can't perfom operations with strings")
                exit(0)
            code = CodeNode(children=[code])

            for i in range((ctx.getChildCount() - 1) // 2):
                op = ctx.getChild(2 * i + 1).getText()
                if op not in ('*', '/', '%'):
                    print("Unknown operation: " + op)
                    exit(0)

                next_expr_type, next_expr_code, next_stack_limit = self.visitMul(ctx.getChild(2 * i + 2))
                if next_expr_type not in (BOOL, INT, LONG, DOUBLE, FLOAT):
                    print("Wrong operand type for " + op + " operation")
                    exit(0)

                common_type = common_cast_type(expr_type, next_expr_type)
                if common_type > expr_type and common_type != INT:
                    code.children.append(CodeNode(cast(expr_type, common_type)))
                code.children.append(next_expr_code)
                if common_type > next_expr_type and common_type != INT:
                    code.children.append(CodeNode(cast(next_expr_type, common_type)))
                    next_stack_limit = max(next_stack_limit, 2)
                if op == '*':
                    code.children.append(CodeNode(letter(common_type) + 'mul'))
                elif op == '/':
                    code.children.append(CodeNode(letter(common_type) + 'div'))
                else:
                    code.children.append(CodeNode(letter(common_type) + 'rem'))
                stack_limit = max(stack_limit, next_stack_limit + type_len(common_type))
                expr_type = common_type
        return expr_type, code, stack_limit

    def visitCastedMul(self, ctx: LanguageParser.CastedMulContext):
        cast_type = self.visitVarType(ctx.getChild(1))
        expr_type, expr_code, stack_limit = self.visitMul(ctx.getChild(3))
        if cast_type != expr_type:
            if cast_type == STRING:
                print("Can't cast to string other types than string")
                exit(0)
            if expr_type == STRING:
                print("Can't cast any type to string")
                exit(0)
            if cast_type == BOOL and expr_type == INT:
                code = CodeNode(*int_to_bool(), children=[expr_code])
            else:
                code = CodeNode(cast(expr_type, cast_type), children=[expr_code])
                stack_limit = max(stack_limit, type_len(cast_type))
            return cast_type, code, stack_limit
        return cast_type, expr_code, stack_limit

    def visitMul(self, ctx: LanguageParser.MulContext):
        if ctx.getChildCount() == 3:
            return self.visitExpression(ctx.getChild(1))

        child = ctx.getChild(0)
        if hasattr(child, 'getRuleIndex'):
            if child.getRuleIndex() == LanguageParser.RULE_var:
                return self.visitVar(child)
            elif child.getRuleIndex() == LanguageParser.RULE_funcCall:
                return self.visitFuncCall(child)
            else:
                print("Unknown parser node")
                exit(0)
        else:
            const_type = const_type_from_parser(child.getSymbol().type)
            if const_type == BOOL:
                return const_type, CodeNode('iconst_0' if child.getText() == 'false' else 'iconst_1'), 1
            elif const_type in (INT, STRING):
                return const_type, CodeNode('ldc ' + child.getText()), 1
            elif const_type == LONG:
                return const_type, CodeNode('ldc2_w ' + child.getText()[1:] + 'l'), 2
            elif const_type == FLOAT:
                return const_type, CodeNode('ldc ' + child.getText() + 'f'), 1
            elif const_type == DOUBLE:
                return const_type, CodeNode('ldc2_w ' + child.getText()[1:]), 2
            else:
                print('Unknown constant type: ' + str(const_type))
                exit(0)

    def visitVar(self, ctx: LanguageParser.VarContext):
        var_name = ctx.getChild(0).getText()
        if ctx.getChildCount() > 1:
            var_field = ctx.getChild(2).getText()
        else:
            var_field = None
        if self.is_visible(var_name):
            var_number = self.get_var_number(var_name)
            var_type = self.current_method.locals[var_number]
            if var_type == UNION:
                if var_field is None:
                    print("You can't access union " + var_name + " without specifying it's field")
                    exit(0)
                elif var_field not in self.unions[var_name]:
                    print("Union " + var_name + " has no field " + var_field)
                    exit(0)
                else:
                    var_type = self.unions[var_name][var_field]

            code = letter(var_type) + 'load' + (' ' if var_number > 3 else '_') + str(var_number)
            return var_type, CodeNode(code), type_len(var_type)
        elif var_name in self.fields:
            if var_field is not None:
                print("Global variables like " + var_name + " can't be unions, so they can't have fields")
                exit(0)
            var_type = self.fields[var_name]
            if self.main_class is None:
                return var_type, CodeNode('getstatic ' + self.classname + '/' + var_name +
                                          ' ' + type_to_string(var_type)), type_len(var_type)
            else:
                return var_type, CodeNode('aload_0', 'getfield ' + self.classname + '/' + var_name +
                                          ' ' + type_to_string(var_type)), type_len(var_type)
        elif self.main_class is not None and var_name in self.main_class.fields:
            if var_field is not None:
                print("Global variables like " + var_name + " can't be unions, so they can't have fields")
                exit(0)
            var_type = self.main_class.fields[var_name]
            return var_type, CodeNode('getstatic ' + self.main_class.classname + '/' + var_name +
                                      ' ' + type_to_string(var_type)), type_len(var_type)
        else:
            print("Variable " + var_name + " is not visible")
            exit(0)

    def visitFuncCall(self, ctx: LanguageParser.FuncCallContext):
        func_name = ctx.getChild(0).getText()
        arg_types, arg_codes, stack_limit = self.visitCallArguments(ctx.getChild(2))
        if func_name not in self.methods:
            if func_name not in self.main_class.methods:
                print("Undefined function: " + func_name)
                exit(0)
                return
            else:
                method = self.main_class.methods[func_name]
                classname = self.main_class.classname
        else:
            method = self.methods[func_name]
            classname = self.classname

        if len(arg_types) != len(method.arguments):
            print("Wrong number of arguments for " + func_name + ". " + str(len(arg_types)) +
                  " instead of " + str(len(method.arguments)))
            exit(0)
        for i in range(len(arg_types)):
            if arg_types[i] != method.arguments[i].type:
                if i % 10 == 0 and i != 10:
                    suffix = 'st'
                elif i % 10 == 1 and i != 11:
                    suffix = 'nd'
                elif i % 10 == 2 and i != 12:
                    suffix = 'd'
                else:
                    suffix = 'th'
                print("Wrong " + str(i + 1) + suffix + " argument type for " + func_name + ".")
                exit(0)
        if method.return_type != VOID:
            stack_limit = max(stack_limit, 1)  # if there no arguments, but we need place to put return value
        code = CodeNode()
        if self.main_class is not None and func_name in self.methods:
            code.children.append(CodeNode('aload_0'))
            command = "invokevirtual "
        else:
            command = "invokestatic "
        code.children += arg_codes
        
        code.code = [command + classname + '/' + func_name + '(' + "".join([type_to_string(i) for i in arg_types]) +
                     ')' + type_to_string(method.return_type)]
        return method.return_type, code, stack_limit

    def visitCallArguments(self, ctx: LanguageParser.CallArgumentsContext):
        types, expressions = [], []
        stack_limit = 0
        for i in range((ctx.getChildCount() + 1) // 2):
            expr_type, expr_code, expr_stack_limit = self.visitExpression(ctx.getChild(2 * i))
            stack_limit = max(stack_limit, expr_stack_limit + sum([type_len(t) for t in types]))
            types.append(expr_type)
            expressions.append(expr_code)
        return types, expressions, stack_limit

    def visitVarType(self, ctx: LanguageParser.VarTypeContext):
        return type_from_parser(ctx.getChild(0).getSymbol().type)

    def visitCondition(self, ctx: LanguageParser.ConditionContext):
        expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(1))
        if expr_type == STRING:
            print("Can't cast string to boolean ")
            exit(0)
        if expr_type not in PRIMITIVE:
            expr_code += [letter(expr_type) + 'const_0', letter(expr_type) + 'cmp' + ('g' if expr_type != LONG else '')]
        cur_method = self.current_method
        cur_method.stack_limit = max(cur_method.stack_limit, stack_limit)
        false_label = "Label" + str(get_next_label_num())
        cur_method.code += expr_code
        cur_method.code.append("ifeq " + false_label)
        self.visitBlock(ctx.getChild(2))
        if ctx.getChildCount() > 3:
            exit_label = "Label" + str(get_next_label_num())
            cur_method.code.append("goto " + exit_label)
            cur_method.code.append(false_label + ":")
            self.visitBlock(ctx.getChild(4))
            cur_method.code.append(exit_label + ":")
        else:
            cur_method.code.append(false_label + ":")

    def visitTreadCall(self, ctx: LanguageParser.TreadCallContext):
        thread_name = ctx.getChild(0).getText()
        if thread_name not in self.threads and (self.main_class is None or thread_name not in self.main_class.threads):
            print("Unknown thread: " + thread_name)
            exit(0)
        main_class_name = self.classname if self.main_class is None else self.main_class.classname
        self.current_method.code += ['new java/lang/Thread',
                                     'dup',
                                     'new ' + main_class_name + '$' + thread_name,
                                     'dup',
                                     'invokespecial ' + main_class_name + '$' + thread_name + '/<init>()V',
                                     'invokespecial java/lang/Thread/<init>(Ljava/lang/Runnable;)V',
                                     'invokevirtual java/lang/Thread/start()V']
        self.current_method.stack_limit = max(self.current_method.stack_limit, 4)

    def visitFunctionDeclaration(self, ctx: LanguageParser.FunctionDeclarationContext):
        func_type = self.visitFuncType(ctx.getChild(0))
        func_name = ctx.getChild(1).getText()
        if func_name in self.methods:
            print("Function " + func_name + " is already defined")
        func_arguments = self.visitArguments(ctx.getChild(3))
        self.methods[func_name] = Method(func_type, func_arguments)

    def visitFunctionDefinition(self, ctx: LanguageParser.FunctionDefinitionContext):
        func_type = self.visitFuncType(ctx.getChild(0))
        func_name = ctx.getChild(1).getText()
        if func_name in self.methods:
            if self.methods[func_name].code is not None:
                print("Function " + func_name + " is already defined")
                print(self.methods[func_name].code)
                exit(0)
        func_arguments = self.visitArguments(ctx.getChild(3))
        if func_name in self.methods and not check_arguments(func_arguments, self.methods[func_name].arguments):
            print("wrong arguments for " + func_name + " function definition")
            exit(0)
        prev_method = self.current_method
        self.methods[func_name] = self.current_method = Method(func_type, func_arguments, [])
        self.set_method_params(func_arguments)

        self.visitBlock(ctx.getChild(5))
        if func_type == VOID:
            self.current_method.code.append("return")

        self.visible_vars.pop()  # we put one level while setting method params
        self.current_method = prev_method

    def visitFuncType(self, ctx: LanguageParser.FuncTypeContext):
        child = ctx.getChild(0)
        if hasattr(child, "getRuleIndex"):
            return type_from_parser(child.getChild(0).getSymbol().type)
        elif child.getSymbol().type == LanguageParser.VoidType:
            return VOID
        else:
            print("illegal function type: " + child.getText())
            exit(0)

    def visitArguments(self, ctx: LanguageParser.ArgumentsContext):
        arguments = []
        for i in range((ctx.getChildCount() + 1) // 2):
            arguments.append(self.visitArgument(ctx.getChild(i * 2)))
        return arguments

    def visitArgument(self, ctx: LanguageParser.ArgumentContext):
        return Argument(self.visitVarType(ctx.getChild(0)), ctx.getChild(1).getText())

    def visitBlock(self, ctx: LanguageParser.BlockContext):
        self.visible_vars.append({})
        for i in range(1, ctx.getChildCount() - 1):
            ctx.getChild(i).accept(self)
        self.visible_vars.pop()

    def visitWrite(self, ctx: LanguageParser.WriteContext):
        expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(1))
        expr_type = type_to_string(expr_type)
        method = self.current_method
        method.stack_limit = max(method.stack_limit, stack_limit + 1)
        return ['getstatic java/lang/System/out Ljava/io/PrintStream;'] + expr_code + \
               ['invokevirtual java/io/PrintStream/print' + ('' if ctx.getChild(0).getText() == 'write' else 'ln') +
                '(' + expr_type + ')V']

    def visitReturnValue(self, ctx: LanguageParser.ReturnValueContext):
        method = self.current_method
        ret_type = self.current_method.return_type
        if ctx.getChildCount() == 1:
            if method.return_type != VOID:
                print("Function can not return void value")
                exit(0)
            method.code.append("return")
        else:
            expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(1))
            if ret_type != expr_type and (ret_type not in PRIMITIVE or expr_type not in PRIMITIVE):
                print("Wrong return type for function")
                exit(0)
            method.stack_limit = max(method.stack_limit, stack_limit)
            expr_code.append("ireturn" if ret_type in PRIMITIVE else "areturn" if ret_type == STRING else None)
            method.code += expr_code

    def visitFunction(self, ctx: LanguageParser.FunctionContext):
        return super().visitFunction(ctx)

    def visitComment(self, ctx: LanguageParser.CommentContext):
        return super().visitComment(ctx)

    def visitThread(self, ctx: LanguageParser.ThreadContext):
        thread_name = ctx.getChild(1).getText()
        if thread_name in self.threads:
            print("Thread " + thread_name + " is already exists")
            exit(0)
        thread_visitor = Visitor(self.classname + '$' + thread_name, self)
        thread_visitor.visitProgram(ctx.getChild(3))
        self.threads[thread_name] = thread_visitor.build_thread_code()

    def visitUnionDeclaration(self, ctx: LanguageParser.UnionDeclarationContext):
        name = ctx.getChild(1).getText()
        if name in self.unions:
            print("Union " + name + " has already been declared")
            exit(0)
        fields = {}
        union_size = 1
        for i in range(3, ctx.getChildCount() - 1):
            field_type, field_name = self.visitUnionField(ctx.getChild(i))
            if field_name in fields:
                print("Union " + name + " has more then one field " + field_name)
                exit(0)
            if field_type == VOID:
                print("Union " + name + " contains void field")
                exit(0)
            if union_size == 1 and field_type in LONG_TYPES:
                union_size = 2
            fields[field_name] = field_type
        self.unions[name] = fields
        method_locals = self.current_method.locals
        self.visible_vars[-1][name] = len(method_locals)
        method_locals += [UNION] * union_size

    def visitUnionField(self, ctx: LanguageParser.UnionFieldContext):
        return self.visitVarType(ctx.getChild(0)), ctx.getChild(1).getText()

    def visitCycle(self, ctx: LanguageParser.CycleContext):
        expr_type, expr_code, stack_limit = self.visitExpression(ctx.getChild(1))
        if expr_type == STRING:
            print("Can't cast string to boolean ")
            exit(0)
        if expr_type not in PRIMITIVE:
            expr_code += [letter(expr_type) + 'const_0', letter(expr_type) + 'cmp' + ('g' if expr_type != LONG else '')]
        cur_method = self.current_method
        cur_method.stack_limit = max(cur_method.stack_limit, stack_limit)
        start_label = "Label" + str(get_next_label_num())
        exit_label = "Label" + str(get_next_label_num())
        cur_method.code.append(start_label + ":")
        cur_method.code += expr_code
        cur_method.code.append("ifeq " + exit_label)
        self.visitBlock(ctx.getChild(2))
        cur_method.code.append("goto " + start_label)
        cur_method.code.append(exit_label + ":")

    def visitRead(self, ctx: LanguageParser.ReadContext):
        self.has_reader = True
        var_name = ctx.getChild(1).getText()
        classname = self.classname if self.main_class is None else self.main_class.classname
        if self.is_visible(var_name):
            var_num = self.get_var_number(var_name)
            var_type = self.current_method.locals[var_num]
        elif var_name in self.fields:
            var_type = self.fields[var_name]
            classname = self.classname
            if self.main_class is not None:
                self.current_method.code.append("aload_0")
        elif self.main_class is not None and var_name in self.main_class.fields:
            var_type = self.main_class.fields[var_name]
            classname = self.main_class.classname
        else:
            print("Variable " + var_name + " isn't visible")
            exit(0)
            return
        self.current_method.code.append("getstatic " + classname + " Sc Ljava/util/Scanner;")
        if var_type == BOOL:
            self.current_method.code.append("invokevirtual java/util/Scanner/nextBoolean()Z")
        elif var_type == INT:
            self.current_method.code.append("invokevirtual java/util/Scanner/nextInt()I")
        elif var_type == LONG:
            self.current_method.code.append("invokevirtual java/util/Scanner/nextLong()J")
        elif var_type == FLOAT:
            self.current_method.code.append("invokevirtual java/util/Scanner/nextFloat()F")
        elif var_type == DOUBLE:
            self.current_method.code.append("invokevirtual java/util/Scanner/nextDouble()D")
        elif var_type == STRING:
            self.current_method.code.append("invokevirtual java/util/Scanner/nextLine()Ljava/lang/String;")
        else:
            print("Wrong type for reading")
            exit(0)
        if var_name not in self.fields and var_name not in self.main_class.fields:
            self.current_method.code.append(letter(var_type) + "store" + ("_" if var_num < 4 else " ") + str(var_num))
        elif var_name in self.fields and self.main_class is not None:
            self.current_method.code.append("putfield " + classname + " " + var_name + " " + type_to_string(var_type))
        else:
            self.current_method.code.append("putstatic " + classname + " " + var_name + " " + type_to_string(var_type))

        self.current_method.stack_limit = max(self.current_method.stack_limit, type_len(var_type), type_len(var_type))

    def visitReleaseLock(self, ctx: LanguageParser.ReleaseLockContext):
        var_name = ctx.getChild(1).getText()
        if self.is_visible(var_name) or self.main_class is not None and var_name in self.fields:
            print("Trying to release a lock of the shadowed variable")
            exit(0)
        if self.main_class is None and var_name not in self.fields or self.main_class is not None \
                and var_name not in self.main_class.fields:
            print("No such lockable variable: " + var_name)
            exit(0)
        else:
            var_type = self.fields[var_name] if self.main_class is None else self.main_class.fields[var_name]
            if var_type != STRING:
                print("Only locks on str objects are available")
                exit(0)
            classname = self.classname if self.main_class is None else self.main_class.classname
            self.current_method.code += ['getstatic ' + classname + ' ' + var_name + " Ljava/lang/String;",
                                         'monitorexit']

    def visitGetLock(self, ctx: LanguageParser.GetLockContext):
        var_name = ctx.getChild(1).getText()
        if self.is_visible(var_name) or self.main_class is not None and var_name in self.fields:
            print("Trying to get a lock of the shadowed variable")
            exit(0)
        if self.main_class is None and var_name not in self.fields or self.main_class is not None \
                and var_name not in self.main_class.fields:
            print("No such lockable variable: " + var_name)
            exit(0)
        else:
            var_type = self.fields[var_name] if self.main_class is None else self.main_class.fields[var_name]
            if var_type != STRING:
                print("Only locks on str objects are available")
                exit(0)
            classname = self.classname if self.main_class is None else self.main_class.classname
            self.current_method.code += ['getstatic ' + classname + ' ' + var_name + " Ljava/lang/String;",
                                         'monitorenter']
