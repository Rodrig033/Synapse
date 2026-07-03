from lexer.lexer import Lexer
from syn_parser.parser import Parser
from visitors.ast_printer import ASTPrinter
from semantic.semantic_analyzer import SemanticAnalyzer
from backend.java_writer import JavaWriter
from backend.java_generator import JavaGenerator

source = """
/*
Programa de prueba de Synapse
*/

int a <- 10 ::
int b <- 5 ::

if gt(a, b) {
    print "mayor" ::
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

# Java Generator
generator = JavaGenerator()
java_code = generator.visit(tree)
print(java_code)

# Ejecutable de Synapse -> Java
with open("Main.java", "w", encoding="utf-8") as file:
    file.write(java_code)