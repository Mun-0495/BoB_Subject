/* calculator with AST */
%{
# include <stdio.h>
# include <stdlib.h>
# include "fb3-1.h"
%}
%union {
 struct ast *a;
 double d;
}
/* declare tokens */
%token <d> NUMBER
%token EOL
%type <a> exp factor term
%left '+' '-'
%left '*' '/'
%nonassoc '|' UMINUS

%type <a> exp

%%
exp: exp '+' exp { $$ = newast('+', $1,$3); }
 | exp '-' exp { $$ = newast('-', $1,$3);}
%%
calclist: /* nothing */
| calclist exp EOL {
 printf("= %4.4g\n", eval($2)); // evaluate and print the AST
 treefree($2); //free up the AST
  printf("> ");
 }
 | calclist EOL { printf("> "); } /* blank line or a comment */
 ;
exp: factor
 | exp '+' factor { $$ = newast('+', $1,$3); }
 | exp '-' factor { $$ = newast('-', $1,$3);}
 | exp '*' exp { $$ = newast('*', $1,$3); }
 | exp '/' exp { $$ = newast('/', $1,$3); }
 | '|' exp { $$ = newast('|', $2, NULL); }
 | '(' exp ')' { $$ = $2; }
 | '-' exp %prec UMINUS{ $$ = newast('M', NULL, $2); }
 | NUMBER { $$ = newnum($1); }
 ;
factor: term
 | factor '*' term { $$ = newast('*', $1,$3); }
 | factor '/' term { $$ = newast('/', $1,$3); }
 ;
term: NUMBER { $$ = newnum($1); }
 | '|' term { $$ = newast('|', $2, NULL); }
 | '(' exp ')' { $$ = $2; }
 | '-' term { $$ = newast('M', $2, NULL); }
 ;
%%

