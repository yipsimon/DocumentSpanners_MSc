grammar formula;
/*
* Parser Rules
*/
formula : regex+ EOF;
regex : (EMPTY | LETTER | concat | star | union | plus | varconf);
concat : '(' regex '.' regex ')' ;
star : '(' regex ')' '*';
union : '(' regex '|' regex ')';
plus : '(' regex ')' '+';
varconf : '{' LETTER ':' regex '}';


/*
* Lexer Rules
*/

fragment LOWERCASE : [a-z];
fragment UPPERCASE : [A-Z];
fragment DIGIT : [0-9];

EMPTY : '/em';

LETTER : (LOWERCASE | UPPERCASE)+;
WS : [ \t\r\n]+ -> skip;
