from semantic.symbol import Symbol
from semantic.semantic_error import SemanticError
from semantic.symbol_table import SymbolTable


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit(self, node):

        method_name = (
            f"visit_"
            f"{type(node).__name__}"
        )

        visitor = getattr(
            self,
            method_name,
            self.generic_visit
        )

        return visitor(node)

    def generic_visit(self, node):
        raise Exception(
            f"No existe análisis para "
            f"{type(node).__name__}"
        )

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    # La declaración debe prohibirse dentro del mismo scope. 
    def visit_VariableDeclaration(self, node):
        existing = (
            self.symbol_table.lookup_current_scope(
                node.name
            )
        )

        if existing:

            raise SemanticError(
                f"Variable "
                f"'{node.name}' "
                f"ya declarada."
            )

        symbol = Symbol(
            node.name,
            node.var_type
        )

        self.symbol_table.define(
            node.name,
            symbol
        )

        value_type = self.visit(node.value)

        if value_type != node.var_type:
            raise SemanticError(
                f"No se puede asignar "
                f"{value_type} "
                f"a "
                f"{node.var_type}"
            )            

    # Literales
    def visit_IntegerLiteral(self, node):
        return "int"
    
    def visit_FloatLiteral(self, node):
        return "float"
    
    def visit_StringLiteral(self, node):
        return "string"
    
    def visit_CharLiteral(self, node):
        return "char"
    
    def visit_BooleanLiteral(self, node):
        return "bool"
    
    def visit_Identifier(self, node):

        symbol = (
            self.symbol_table.lookup(
                node.name
            ))
        
        if not symbol:
            raise SemanticError(
                f"Variable"
                f"'{node.name}' "
                f"no declarada."
            )
        
        return symbol.symbol_type
    
    def visit_PrintStatement(self, node):
        self.visit(node.expression)

    def visit_ComparisonExpression(self, node):

        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != right_type:
            raise SemanticError(
                f"No se puede comparar un {left_type} "
                f"con un {right_type}."
            )

        if left_type not in ("int", "float", "char", "string"):
            raise SemanticError(
                f"El operador '{node.operator}' "
                f"no admite operandos de tipo "
                f"{left_type}."
            )
        
        # Toda comparación produce un booleano
        return "bool"
    
    def visit_IfStatement(self, node):
        condition_type = self.visit(node.condition)
        
        # Compara el tipo 
        if condition_type != "bool":
            raise SemanticError(
                "La condición del if debe ser booleana."
            )

        # Scope del THEN
        self.symbol_table.enter_scope()

        for statement in node.then_body:
            self.visit(statement)

        self.symbol_table.exit_scope()

        # Scope del ELSE
        if node.else_body:
            self.symbol_table.enter_scope()

            for statement in node.else_body:
                self.visit(statement)

            self.symbol_table.exit_scope()

    def visit_WhileStatement(self, node):
        condition_type = self.visit(node.condition)

        # Compara el tipo
        if condition_type != "bool":
            raise SemanticError(
                "La condición del while debe ser booleana."
            )

        self.symbol_table.enter_scope()

        for statement in node.body:
            self.visit(statement)

        self.symbol_table.exit_scope()

    def visit_Assignment(self, node):
        symbol = (
            self.symbol_table.lookup(
                node.name
            )
        )

        if not symbol:
            raise SemanticError(
                f"Variable "
                f"'{node.name}' "
                f"no declarada. "
            )
        
        value_type = self.visit(node.value)

        if value_type != symbol.symbol_type:
            raise SemanticError(
            f"No se puede asignar "
            f"{value_type} "
            f"a "
            f"{symbol.symbol_type}"
        )

    def visit_ArithmeticExpression(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        destination = self.symbol_table.lookup(node.destination)

        if not destination:
            raise SemanticError(
                f"Variable '{node.destination}' no declarada."
            )
        
        destination_type = destination.symbol_type

        if destination_type != left_type:
            raise SemanticError(
                f"No se puede almacenar un resultado "
                f"de tipo {left_type} "
                f"en una variable de tipo "
                f"{destination_type}."
        )

        if left_type != right_type:
            raise SemanticError(
            f"No se puede operar un {left_type} con un "
            f"{right_type}."
        )

        if left_type not in ("int", "float"):
            raise SemanticError(
                f"El operador '{node.operator}' "
                f"solo admite operandos numéricos."
            )        

        return destination_type
    
    def visit_BooleanExpression(self, node):

        left_type = self.visit(node.left)

        if left_type != "bool":
            raise SemanticError(
                "La expresión izquierda debe ser booleana."
            )

        if node.operator != "not":

            right_type = self.visit(node.right)

            if right_type != "bool":
                raise SemanticError(
                    "La expresión derecha debe ser booleana."
                )

        return "bool"