class ASTNodes:
    pass

class Program(ASTNodes):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program ({self.statements})"