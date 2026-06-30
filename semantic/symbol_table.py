class SymbolTable:
    def __init__(self):
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({}) 

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def define(self, name, symbol):
        self.scopes[-1][name] = symbol

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def lookup_current_scope(self, name):
        return self.scopes[-1].get(name)

    # Importante para las funciones
    def current_scope(self):
        return self.scopes[-1]

    def __repr__(self):
        return str(self.scopes)