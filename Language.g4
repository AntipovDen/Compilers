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
    | LongType
    | FloatType
    | DoubleType
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
    : UnionType LowerName '{' unionField+ '}'
    ;

unionField
    : varType LowerName ';'
    ;

assignment
    : LowerName ('.' LowerName)? '=' expression
    ;

expression
    : andExpr (('||'|'V') andExpr)*
    | assignment
    ;

andExpr
    : compExpr (('&&'|'|') compExpr)*
    ;

compExpr
    : '!'? arithmExpr (CompOp arithmExpr)*
    ;

arithmExpr
    : summand (('+' | '-') summand)*
    ;

summand
    : (mul | castedMul) (('*'|'/'|'%') (mul | castedMul))*
    ;

castedMul
    : '(' varType ')' mul
    ;

mul
    : Bool
    | Integer
    | String
    | Long
    | Float
    | Double
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
LongType    : 'long' ;
FloatType   : 'float' ;
DoubleType  : 'double' ;
UnionType   : 'union' ;
Thread      : 'thread' ;

Integer     : '0' | [-]?[1-9][0-9]*;
String      : '"'(~('"'))*'"';
Bool        : 'true' | 'false';
Long        : 'l0' | 'l'[-]?[1-9][0-9]*;
Float       : [-]?('0' | [1-9][0-9]*)'.'[0-9]+;
Double      : 'd'[-]?('0' | [1-9][0-9]*)'.'[0-9]+;

CompOp      : '==' | '!=' | '>' | '<' | '>=' | '<=';

LowerName   : [a-z][A-Za-z0-9_]*;
UpperName   : [A-Z][A-Za-z0-9_]*;

CommentText :  '#'(~('\n'))*('\n'|EOF) ;

WS          : [ \t\r\n]+ -> skip ;
