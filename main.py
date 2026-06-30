from lexer.lexer import Lexer
from syn_parser.parser import Parser
from visitors.ast_printer import ASTPrinter
from semantic.semantic_analyzer import SemanticAnalyzer

source = """
/*
Programa de prueba de Synapse
*/

int a <- 10 ::
int b <- 5 ::

if and(
    gt(a, b),
    lt(b, a)
) {

    print "OK" ::

}

"""

lexer = Lexer(source)
tokens = lexer.tokenize()

# AST
parser = Parser(tokens)
tree = parser.parse()

printer = ASTPrinter()
printer.print(tree)

# Semantic
semantic = SemanticAnalyzer()
semantic.visit(tree)
print(semantic.symbol_table)

for token in tokens:
    print(token)