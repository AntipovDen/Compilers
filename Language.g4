grammar Language;

/*
My corsework is a compiler of my language into JVM bytecode.
The program written on my language consists of commands, function definitions and declarations and thread definitions.
All the commands that are not inside some function are in the "main" function that will be called first.
In every function all the variables that were declared before function definition are visible global variables.
All the variables that are declared after function cannot be used inside it.
Also there are some strong constraints about the codestyle: all the names of variables, functions and union fields
must start with lowercase letter and names of threads must start with uppercase one.
The precedense of operators is the same as in java.
*/


program
    : (function | thread | command | comment)*
    ;


function
    : functionDeclaration
    | functionDefinition
    ;

functionDeclaration
    : funcType LowerName '(' arguments ')' ';'
    ;

functionDefinition
    : funcType LowerName '(' arguments ')' block
    ;

funcType
    : varType
    | VoidType
    ;

varType
    : IntType
    | BoolType
    | StringType
    ;

arguments
    :
    | argument (',' argument)*
    ;

argument
    : varType LowerName
    ;


block
    : '{' command* '}'
    ;

thread
    : Thread UpperName '(' arguments ')' block
    ;

command
    : varDeclaration ';'
    | unionDeclaration ';'
    | assignment ';'
    | condition
    | cycle
    | read ';'
    | write ';'
    | returnValue ';'
    | funcCall ';'
    | treadCall ';'
    | block
    ;

varDeclaration
    : varType LowerName ('=' expression)?
    ;

unionDeclaration
    : UnionType LowerName '{' (varDeclaration ';')+ '}'
    ;

assignment
    : LowerName '=' expression
    ;

expression
    : andExpr ('||' andExpr)*
    | assignment
    ;

andExpr
    : compExpr ('&&' compExpr)*
    ;

compExpr
    : arithmExpr (CompOp arithmExpr)*
    ;

arithmExpr
    : summand (('+' | '-') summand)*
    ;

summand
    : mul (('*'|'/'|'%') mul)*
    | mul
    ;

mul
    : Bool
    | Integer
    | String
    | var
    | funcCall
    | '(' expression ')'
    ;

var
    : LowerName ('.' LowerName)?
    ;

funcCall
    : LowerName '(' callArguments ')'
    ;

callArguments
    :
    | expression (',' expression)*
    ;

treadCall
    : UpperName '(' callArguments ')'
    ;

condition
    : 'if' expression block ('else' block)?
    ;

cycle
    : 'while' expression block
    ;

read
    : 'read' LowerName
    ;

write
    : 'write' expression
    ;

returnValue
    : 'return' (expression)?
    ;

comment
    : CommentText
    ;
//LEXER RULES

VoidType    : 'void' ;
IntType     : 'int' ;
BoolType    : 'bool' ;
StringType  : 'str' ;
UnionType   : 'union' ;
Thread      : 'thread' ;

Integer     : '0' | [-]?[1-9][0-9]*;
String      : [\"].*[\"];
Bool        : 'true' | 'false';

CompOp      : '==' | '!=' | '>' | '<' | '>=' | '<=';

LowerName   : [a-z][A-Za-z0-9_]*;
UpperName   : [A-Z][A-Za-z0-9_]*;

CommentText :  '#'.*'\n' ;

WS          : [ \t\r\n]+ -> skip ;
