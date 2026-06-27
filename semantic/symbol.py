class Symbol:
    def __init__(self, name, symbol_type):
        self.name = name
        self.symbol_type = symbol_type

    def __repr__(self):
        return (
            f"Symbol("
            f"name={self.name}, "
            f"type={self.symbol_type}"
            f")"
        )    