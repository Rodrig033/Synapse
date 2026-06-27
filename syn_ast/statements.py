from .nodes import ASTNodes

class Statement(ASTNodes):
    pass

class VariableDeclaration(Statement):
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name 
        self.value = value

    def __repr__(self):
         return (
             f"VariableDeclaration("
             f"type={self.var_type}, "
             f"name={self.name}, "
             f"value={self.value}"
             f")"
         )  

class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return (f"PrintStatement("
                f"{self.expression}"
                f")")    

class IfStatement(Statement):
    def __init__(self, condition, then_body, else_body = None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
    
    def __repr__(self):
        return (
            f"IfStatement("
            f"condition={self.condition}, "
            f"then_body={len(self.then_body)}, "
            f"else_body={len(self.else_body) if self.self.else_body else 0} statements"
            f")"
        )

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return (
            f"WhileStatement("
            f"condition={self.condition}, "
            f"body={self.body}"
            f")"
        )
      
class Assignment(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return (
            f"Assignment ("
            f"name={self.name}, "
            f"value={self.value}"
            f")"
        )
    
class ArithmeticExpression(Statement):
    def __init__(self, operator, destination, left, right):
        self.operator = operator
        self.destination = destination
        self.left = left
        self.right = right

    def __repr__(self):
        return (
            f"ArithmeticExpression("
            f"operator={self.operator}, "
            f"destination={self.destination}, "
            f"left={self.left}, "
            f"right={self.right}"
            f")"
        )