from backend.java_writer import JavaWriter

class JavaGenerator:
    def __init__(self):
        self.writer = JavaWriter()
    
    def java_type(self, synapse_type):

        mapping = {
            "int": "int",
            "float": "float",
            "bool": "boolean",
            "char": "char",
            "string": "String"
        }

        return mapping[synapse_type]
    
    def java_arithmetic(self, operator):
        mapping = {
            "add" : "+",
            "sub" : "-",
            "mul" : "*",
            "div" : "/",
            "mod" : "%"
        }

        return mapping[operator]
    
    def java_operator(self, operator):
        mapping = {
            "gt": ">",
            "lt": "<",
            "eq": "==",
            "neq": "!=",
            "ge": ">=",
            "le": "<="
        }

        return mapping[operator]

    def visit(self, node):

        method_name = (
            f"visit_"
            f"{type(node).__name__}"
        )

        visitor = getattr(self, 
                          method_name, 
                          self.generic_visit
                          )
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception(
            f"No existe generador para "
            f"{type(node).__name__}"
        )
    
    def visit_Program(self, node):
        self.writer.writeln("public class Main {")
        self.writer.indent()
        self.writer.writeln("public static void main(String[] args) {")
        self.writer.indent()

        for statement in node.statements:
            self.visit(statement)
        
        self.writer.dedent()
        self.writer.writeln("}")
        self.writer.dedent()
        self.writer.writeln("}")

        return self.writer.result()
    
    # Statements
    def visit_VariableDeclaration(self, node):
        java_type = self.java_type(node.var_type)
        value = self.visit(node.value)
        self.writer.writeln(f"{java_type} {node.name} = {value};")

    def visit_Assignment(self, node):
        value = self.visit(node.value)
        self.writer.writeln(
            f"{node.name} = {value};"
        )
    
    def visit_PrintStatement(self, node):
        value = self.visit(node.expression)
        self.writer.writeln(
        f"System.out.println({value});"
        )

    # Expressions
    def visit_IntegerLiteral(self, node):
        return str(node.value)

    def visit_FloatLiteral(self, node):
        return f"{node.value}f"
    
    def visit_StringLiteral(self, node):
        return f'"{node.value}"'
    
    def visit_CharLiteral(self, node):
        return f"'{node.value}'"

    def visit_BooleanLiteral(self, node):
        return str(node.value).lower()
    
    def visit_Identifier(self, node):
        return node.name
    
    def visit_ArithmeticExpression(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        operator = self.java_arithmetic(node.operator)

        self.writer.writeln(
            f"{node.destination} = {left} {operator} {right};"
        )
    def visit_ComparisonExpression(self, node):
        operators = {
            "gt": ">",
            "lt": "<",
            "eq": "==",
            "neq": "!=",
            "ge": ">=",
            "le": "<="
        }

        left = self.visit(node.left)
        right = self.visit(node.right)

        operator = operators[node.operator]

        return f"{left} {operator} {right}"
    
    def visit_BooleanExpression(self, node):
        operators = {
            "and" : "&&",
            "or"  : "||"
        }

        if node.operator == "not":
            expression = self.visit(node.left)
            return f"!({expression})"
        
        left = self.visit(node.left)
        right = self.visit(node.right)

        operator = operators[node.operator]
        
        return f"({left}) {operator} ({right})"
    
    def visit_IfStatement(self, node):
        condition = self.visit(node.condition)

        self.writer.writeln( f"if ({condition}) {{")
        self.writer.indent()

        for statement in node.then_body:
            self.visit(statement)
        
        self.writer.dedent()
        self.writer.writeln("}")

        if node.else_body:
            self.writer.writeln("else {")
            self.writer.indent()

            for statement in node.else_body:
                self.visit(statement)
            
            self.writer.dedent()
            self.writer.writeln("}")

    # While y scopes ...