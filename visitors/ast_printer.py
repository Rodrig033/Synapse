class ASTPrinter:

    def print(self, node):
        self.visit(node, "")

    def visit(self, node, prefix=""):

        method_name = (
            f"visit_"
            f"{type(node).__name__}"
        )

        visitor = getattr(
            self,
            method_name,
            self.generic_visit
        )

        return visitor(node, prefix)

    def generic_visit(self, node, prefix=""):
        print(
            f"No existe un visitor "
            f"para {type(node).__name__}"
        )

    def visit_Program(self, node, prefix):

        print("Program")

        for statement in node.statements:
            self.visit(statement) 

    def visit_VariableDeclaration(
    self,
    node,
    prefix
    ):

        print(
            prefix +
            "├── VariableDeclaration"
        )

        print(
            prefix +
            f"│   ├── Type: "
            f"{node.var_type}"
        )

        print(
            prefix +
            f"│   ├── Name: "
            f"{node.name}"
        )

        print(
            prefix +
            "│   └── Value:"
        )

        self.visit(node.value,
                   prefix + "│       ")

    def visit_IntegerLiteral(
        self,
        node,
        prefix
    ):

        print(
            prefix + 
            f"IntegerLiteral: "
            f"{node.value}"
        )

    def visit_FloatLiteral(
    self,
    node,
    prefix 
    ):

        print(
            prefix +
            f"FloatLiteral: "
            f"{node.value}"
        )

    def visit_StringLiteral(
    self,
    node, 
    prefix
    ):

        print(
            prefix +
            f'StringLiteral: '
            f'"{node.value}"'
        )

    def visit_CharLiteral(
        self,
        node,
        prefix
    ):

        print(
            prefix +
            f"CharLiteral: "
            f"'{node.value}'"
        )

    def visit_BooleanLiteral(
    self,
    node,
    prefix
    ):

        print(
            prefix + 
            f"BooleanLiteral: "
            f"{node.value}"
        )

    def visit_Identifier(
    self,
    node, 
    prefix 
    ):

        print(
            prefix +
            f"Identifier: "
            f"{node.name}"
        )

    def visit_PrintStatement(
    self,
    node,
    prefix
    ):

        print(
            prefix +
            "    └── PrintStatement"
        )

        self.visit(
            node.expression,
            prefix + "        "
        )

    def visit_ComparisonExpression(
    self,
    node,
    prefix
    ):

        print(
            prefix +
            "└── ComparisonExpression"
        )

        print(
            prefix +
            f"    ├── Operator: "
            f"{node.operator}"
        )

        self.visit(
            node.left,
            prefix + "    │   "

        )

        self.visit(
            node.right,
            prefix + "    │   "
        )

    def visit_IfStatement(
    self,
    node,
    prefix
    ):

        print(
            prefix +
            "└── IfStatement"
        )

        print(
            prefix +
            "    ├── Condition"
        )

        self.visit(
            node.condition,
            prefix + "    │   "
        )

        print(
            prefix +
            "    └── Body"
        )

        for stmt in node.then_body:
            self.visit(stmt,
                       prefix + "        ")

    def visit_WhileStatement(
    self,
    node,
    prefix
    ):

        print(
            prefix +
            "└── WhileStatement"
        )

        print(
            prefix +
            "    ├── Condition"
        )

        self.visit(
            node.condition
        )

        print(
            prefix +
            "    └── Body"
        )

        for stmt in node.body:
            self.visit(
                stmt,
                prefix + "        "
            )                                                         
    def visit_Assignment(
        self,
        node,
        prefix
    ):

        print(
            prefix +
            "├── Assignment"
        )

        print(
            prefix +
            f"│   ├── Name: {node.name}"
        )

        print(
            prefix +
            "│   └── Value:"
        )

        self.visit(
            node.value,
            prefix + "│       "
        )
    
    # Debes crear visit_arithmetic
    def visit_ArithmeticExpression(self, node, prefix):
        print(prefix + "├── ArithmeticExpression")

        print(prefix + f"│   ├── Operator: {node.operator}")

        print(prefix + "│   ├── Left:")
        self.visit(node.left, prefix + "│   │   ")

        print(prefix + "│   └── Right:")
        self.visit(node.right, prefix + "    ")
            