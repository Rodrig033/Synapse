class JavaWriter:
    def __init__(self):
        self.lines = []
        self.indent_level = 0

    def writeln(self, text=""):
        indent = "    " * self.indent_level
        self.lines.append(indent + text)

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        if self.indent_level > 0:
            self.indent_level -= 1

    def result(self):
        return "\n".join(self.lines)
    
    def clear(self):
        self.lines.clear()
        self.indent_level = 0