class Token:

    def __init__(self, token_type, lexeme):
        self.type = token_type
        self.lexeme = lexeme

    def __repr__(self):
        return f"<{self.type.name}, {self.lexeme}>"