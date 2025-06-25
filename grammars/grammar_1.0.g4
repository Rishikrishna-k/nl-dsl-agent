// grammar for version 1.0

grammar MedicalClaimsDSL;

// Parser Rules
rule: RULE ruleName ruleBody END;

ruleName: IDENTIFIER;

ruleBody: whenClause thenClause (elseClause)?;

whenClause: WHEN condition;
thenClause: THEN action (AND action)*;
elseClause: ELSE action (AND action)*;

condition: simpleCondition
         | compoundCondition
         | existsCondition
         | forEachCondition;

simpleCondition: fieldPath operator value
               | fieldPath operator fieldPath
               | fieldPath IN listValue
               | fieldPath MATCHES regexValue;

compoundCondition: condition (AND | OR) condition
                 | LPAREN condition RPAREN;

existsCondition: EXISTS entityName WHERE condition;

forEachCondition: FOR EACH itemName IN collectionPath condition;

action: approveAction
      | rejectAction
      | setAction
      | flagAction
      | continueAction
      | ifAction;

approveAction: APPROVE;
rejectAction: REJECT stringValue;
setAction: SET assignment (AND SET assignment)*;
flagAction: FLAG stringValue (AND setAction)?;
continueAction: CONTINUE;
ifAction: IF condition THEN action (AND action)* (ELSE action (AND action)*)? END;

assignment: fieldPath ASSIGN value;

fieldPath: IDENTIFIER (DOT IDENTIFIER)*;
collectionPath: fieldPath;
entityName: IDENTIFIER;
itemName: IDENTIFIER;

operator: EQ | NE | GT | LT | GTE | LTE;

value: stringValue
     | numberValue
     | booleanValue
     | dateValue
     | fieldPath;

stringValue: STRING;
numberValue: NUMBER;
booleanValue: TRUE | FALSE;
dateValue: DATE;
listValue: LBRACKET (value (COMMA value)*)? RBRACKET;
regexValue: STRING;

// Lexer Rules
RULE: 'RULE';
WHEN: 'WHEN';
THEN: 'THEN';
ELSE: 'ELSE';
END: 'END';
IF: 'IF';
FOR: 'FOR';
EACH: 'EACH';
IN: 'IN';
WHERE: 'WHERE';
EXISTS: 'EXISTS';
APPROVE: 'APPROVE';
REJECT: 'REJECT';
SET: 'SET';
FLAG: 'FLAG';
CONTINUE: 'CONTINUE';
AND: 'AND';
OR: 'OR';
IN: 'IN';
MATCHES: 'MATCHES';

// Operators
EQ: '==';
NE: '!=';
GT: '>';
LT: '<';
GTE: '>=';
LTE: '<=';
ASSIGN: '=';

// Delimiters
LPAREN: '(';
RPAREN: ')';
LBRACKET: '[';
RBRACKET: ']';
DOT: '.';
COMMA: ',';

// Values
TRUE: 'true';
FALSE: 'false';
STRING: '"' (~["\\\r\n] | '\\' .)* '"';
NUMBER: [0-9]+ ('.' [0-9]+)?;
DATE: [0-9]{4} '-' [0-9]{2} '-' [0-9]{2};
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;

// Whitespace and comments
WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;