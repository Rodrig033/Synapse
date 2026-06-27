from .nodes import ASTNodes

class Expression(ASTNodes):
    pass

class IntegerLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IntegerLiteral({self.value})"

class StringLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):    
        return f"StringLiteral ({self.value})"

class Identifier(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__ (self):
        return f"Identifier({self.name})"

class ComparisonExpression(Expression):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right
    
    def __repr__(self):
        return (f"ComparisonExpression("
                f"{self.operator}, "
                f"{self.left}, "
                f"{self.right}"
                f")")


class Program(Expression):
    def __init__(self, statements):
        
        self.statements = statements

    def __repr__(self):
        return (
            f"Program("
            f"statements={self.statements}"
            f")"
        )

class FloatLiteral(Expression):
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return f"FloatLiteral ({self.value})"
        
class CharLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"CharLiteral('{self.value}')"
        
class BooleanLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"BooleanLiteral({self.value})"
    
class ArithmeticExpression(Expression):
    def __init__ (self, operator, destination, left, right):
        self.operator = operator
        self.destionation = destination
        self.left = left
        self.right = right

""" 
FloatLiteral
CharLiteral
BooleanLiteral
BinaryExpression
CallExpression
"""