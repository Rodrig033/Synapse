from syn_parser.parser_error import ParserError
from syn_ast.nodes import Program
from lexer.token_type import TokenType
from syn_ast.statements import VariableDeclaration
from syn_ast.expressions import (
    IntegerLiteral,
    StringLiteral,
    Identifier,
    FloatLiteral,
    CharLiteral,
    BooleanLiteral,
    ComparisonExpression,
    BooleanExpression
)
from syn_ast.statements import PrintStatement
from syn_ast.statements import IfStatement
from syn_ast.statements import WhileStatement
from syn_ast.statements import Assignment
from syn_ast.statements import ArithmeticExpression

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current = tokens[0]

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current = self.tokens[self.position]

    def match(self, expected):
        if self.current.type == expected:
            token = self.current
            self.advance()
            return token
        
        raise ParserError(
            f"Se esperaba {expected}" 
            f"y se encontró {self.current.type}"
        )

    def parse(self):
        return self.program()

    def program(self):
        statements = []

        while self.current.type != TokenType.EOF:
            statements.append(self.statement())
            
        return Program(statements)
        
    def statement(self):

        if self.current.type in {
            TokenType.TIPO_INT,
            TokenType.TIPO_FLOAT,
            TokenType.TIPO_BOOL,
            TokenType.TIPO_CHAR,
            TokenType.TIPO_STRING
        }:
            return self.variable_declaration()

        elif self.current.type == TokenType.PRINT:
            return self.print_statement()

        elif self.current.type == TokenType.IF:
            return self.if_statement()
                
        elif self.current.type == TokenType.WHILE:
            return self.while_statement()
        
        elif self.current.type == TokenType.IDENTIFICADOR:
            return self.assignment_statement()
        
        elif self.current.type in {
            TokenType.ADD,
            TokenType.SUB,
            TokenType.MUL,
            TokenType.DIV,
            TokenType.MOD
        }:
            return self.arithmetic_statement()
    

        raise ParserError(
            f"Instrucción inválida: "
            f"{self.current.lexeme}"
        )

    def expression(self):
        token = self.current

        if token.type == TokenType.ENTERO:
            self.advance()
            return IntegerLiteral(
                token.lexeme
            )
        
        elif token.type == TokenType.REAL:
            self.advance()
            return FloatLiteral(
                token.lexeme
            )
        

        elif token.type == TokenType.CADENA:
            self.advance()
            return StringLiteral(
                token.lexeme
            )
        
        elif token.type == TokenType.CARACTER:
            self.advance()
            return CharLiteral(
                token.lexeme
            )
        
        elif token.type == TokenType.BOOLEANO:
            self.advance()
            return BooleanLiteral(
                token.lexeme
            )

        elif token.type == TokenType.IDENTIFICADOR:
            self.advance()
            return Identifier(
                token.lexeme
            )
        
        elif token.type in {
            TokenType.OP_GT,
            TokenType.OP_LT,
            TokenType.OP_EQ,
            TokenType.OP_NEQ,
            TokenType.OP_GE,
            TokenType.OP_LE
        }:
            
            return self.comparison_expression()
        
        elif token.type in {
            TokenType.AND,
            TokenType.OR,
            TokenType.NOT
        }:
            return self.boolean_expression()
        
        raise ParserError(
            f"Expresión inválida: "
            f"{token.lexeme}"
        )



    def print_statement(self):

        self.match(TokenType.PRINT)
        expr = self.expression()
        self.match(
            TokenType.FIN_SENTENCIA
        )
        
        return PrintStatement(expr)
    
    def variable_declaration(self):

        var_type = self.current.lexeme
        self.advance()

        name = self.match(
            TokenType.IDENTIFICADOR 
        ).lexeme

        self.match(
            TokenType.ASIGNACION
        )

        value = self.expression()

        self.match(
            TokenType.FIN_SENTENCIA
        )

        return VariableDeclaration(
            var_type,
            name, 
            value
        )
        
    def comparison_expression(self):
        operator = self.current.lexeme
        self.advance()

        self.match(
            TokenType.PARENTESIS_IZQ
        )

        left = self.expression()

        self.match(
            TokenType.COMA
        )

        right = self.expression()

        self.match(
            TokenType.PARENTESIS_DER
        )

        return ComparisonExpression(operator, left, right)
    
    def boolean_expression(self):
        operator = self.current.lexeme
        self.advance()

        self.match(
            TokenType.PARENTESIS_IZQ
        )

        left = self.condition()
        right = None

        if operator != "not":
            self.match(
                TokenType.COMA
            )

            right = self.condition()

        self.match(
            TokenType.PARENTESIS_DER
        )

        return BooleanExpression(operator, left, right)
    

    def condition(self):

        expr = self.expression()

        return expr

    def if_statement(self):

        self.match(TokenType.IF)

        condition = self.condition()
        self.match(
            TokenType.LLAVE_IZQ
        )

        then_body = []

        while (
            self.current.type != TokenType.LLAVE_DER
        ):
            then_body.append(
                self.statement()
            )

        self.match(
            TokenType.LLAVE_DER
        )

        else_body = None

        if self.current.type == TokenType.ELSE:

            self.match(
                TokenType.ELSE
            )

            self.match(
                TokenType.LLAVE_IZQ
            )

            else_body = []

            while (
                self.current.type != TokenType.LLAVE_DER
            ):
                else_body.append(
                    self.statement()
                )

            self.match(
                TokenType.LLAVE_DER
            )

        return IfStatement(
            condition,
            then_body,
            else_body
        )
    def while_statement(self):

        self.match(
            TokenType.WHILE
        )

        condition = self.condition()

        self.match(
            TokenType.LLAVE_IZQ
        )

        body = []

        while (
            self.current.type
            != TokenType.LLAVE_DER
        ):
            body.append(
                self.statement()
            )

        self.match(
            TokenType.LLAVE_DER
        )

        return WhileStatement(
            condition,
            body
        )
    
    def assignment_statement(self):
        name = self.match(
            TokenType.IDENTIFICADOR
        ).lexeme

        self.match(
            TokenType.ASIGNACION
        )

        value = self.expression()

        self.match(
            TokenType.FIN_SENTENCIA
        )

        return Assignment(
            name,
            value
        )
    
    def arithmetic_statement(self):

        # add, sub, mul, div, mod
        operator = self.current.lexeme
        self.advance()

        self.match(
            TokenType.PARENTESIS_IZQ
        )

        destination = self.match(
            TokenType.IDENTIFICADOR
        ).lexeme

        self.match(
            TokenType.COMA
        )

        left = self.expression()

        self.match(
            TokenType.COMA
        )

        right = self.expression()

        self.match(
            TokenType.PARENTESIS_DER
        )

        self.match(
            TokenType.FIN_SENTENCIA
        )

        return ArithmeticExpression(
            operator,
            destination,
            left,
            right
        )
    