from lexer.lexer import Lexer
from syn_parser.parser import Parser
from visitors.ast_printer import ASTPrinter
from semantic.semantic_analyzer import SemanticAnalyzer

source = """
/*
Programa de prueba de Synapse
*/

int a <- 15 ::

if gt(a, 20){
    int x <- 20 ::
    print x ::
}

print x ::

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