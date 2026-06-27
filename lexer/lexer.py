from lexer.token import Token
from lexer.token_type import TokenType
from lexer.errors import LexicalError

KEYWORDS = {
    "int": TokenType.TIPO_INT,
    "float": TokenType.TIPO_FLOAT,
    "bool": TokenType.TIPO_BOOL,
    "char": TokenType.TIPO_CHAR,
    "string": TokenType.TIPO_STRING,
    "void": TokenType.TIPO_VOID,

    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,

    "print": TokenType.PRINT,
    "input": TokenType.INPUT,

    "load": TokenType.LOAD,
    "store": TokenType.STORE,
    "mov": TokenType.MOV,
    "add": TokenType.ADD,
    "sub": TokenType.SUB,
    "mul": TokenType.MUL,
    "div": TokenType.DIV,
    "mod": TokenType.MOD,
    "cmp": TokenType.CMP,
    "jump": TokenType.JUMP,
    "call": TokenType.CALL,
    "push": TokenType.PUSH,
    "pop": TokenType.POP,

    "eq": TokenType.OP_EQ,
    "neq": TokenType.OP_NEQ,
    "lt": TokenType.OP_LT,
    "gt": TokenType.OP_GT,
    "le": TokenType.OP_LE,
    "ge": TokenType.OP_GE,

    "true": TokenType.BOOLEANO,
    "false": TokenType.BOOLEANO
}

class Lexer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.current = self.source[0] if source else None

    # Advance 
    def advance(self):
            self.position += 1
            if self.position >= len(self.source):
                self.current = None
            else:
                self.current = self.source[self.position]

    # Avanzar espacio por espacio
    def skip_whitespace(self):

            while (
                self.current is not None
                and self.current.isspace()
            ):
                self.advance()

    # Reconocer enteros
    def number(self):

        lexema = ""
        decimal = False

        while (
            self.current is not None
            and (
                self.current.isdigit()
                or self.current == "."
            )
        ):

            if self.current == ".":

                if decimal:
                    raise LexicalError(
                        "Número real inválido."
                    )

                decimal = True

            lexema += self.current
            self.advance()

        if decimal:
            return Token(
                TokenType.REAL,
                lexema
            )

        return Token(
            TokenType.ENTERO,
            lexema
        )
    
    # Reconocer cadenas
    def string(self):

        lexema = ""

        # Consumimos la primera "
        self.advance()

        while (
            self.current is not None
            and self.current != '"'
        ):
            lexema += self.current
            self.advance()

        if self.current is None:
            raise LexicalError(
                "Cadena sin cerrar."
            )

        # Consumimos la segunda "
        self.advance()

        return Token(
            TokenType.CADENA,
            lexema
        )
            
    # Reconocer identificadores
    def identifier(self):

        lexema = ""

        while (
            self.current is not None
            and (
                self.current.isalnum()
                or self.current == "_"
            )
        ):
            lexema += self.current
            self.advance()

        token_type = KEYWORDS.get(
            lexema,
            TokenType.IDENTIFICADOR
        )

        return Token(
            token_type,
            lexema
        )
        
        # Método principal 
    def tokenize(self):

            tokens = []

            while self.current is not None:

                if self.current.isspace():
                    self.skip_whitespace()
                    continue

                if self.current.isdigit():
                    tokens.append(
                        self.number()
                    )
                    continue

                if (
                    self.current.isalpha()
                    or self.current == "_"
                ):
                    tokens.append(
                        self.identifier()
                    )
                    continue

                if self.current == "<":

                    self.advance()

                    if self.current == "-":
                        self.advance()

                        tokens.append(
                            Token(
                                TokenType.ASIGNACION,
                                "<-"
                            )
                        )
                        continue

                    raise LexicalError(
                        "Se esperaba '-'"
                    )
                
                if self.current == "'":
                    tokens.append(
                        self.character()
                    )
                    continue

                # Paréntesis izquierdo
                if self.current == "(":
                    tokens.append(
                        Token(
                            TokenType.PARENTESIS_IZQ, "("
                        )
                    )
                    self.advance()
                    continue

                # Paréntesis derecho
                if self.current == ")":
                    tokens.append(
                        Token(
                            TokenType.PARENTESIS_DER, ")"
                        )
                    )
                    self.advance()
                    continue

                # Coma
                if self.current == ",":
                    tokens.append(
                        Token(
                            TokenType.COMA, ","
                        )
                    )
                    self.advance()
                    continue


                # Llave izquierda
                if self.current == "{":
                    tokens.append(
                        Token(
                            TokenType.LLAVE_IZQ, "{"
                        )
                    )
                    self.advance()
                    continue

                # Llave derecha
                if self.current == "}":
                    tokens.append(
                        Token(
                            TokenType.LLAVE_DER, "}"
                        )
                    )
                    self.advance()
                    continue

                # Cadena de texto
                if self.current == '"':
                    tokens.append(
                        self.string()
                        )
                    continue
                
                # Comentarios de línea
                if (self.current == "/" and self.peek() == "/"):
                    self.skip_line_comment()
                    continue

                # Comentarios de bloque
                if (self.current == "/" and self.peek() == "*"):
                    self.skip_block_comment()
                    continue

                if self.current == ":":

                    self.advance()

                    if self.current == ":":
                        self.advance()

                        tokens.append(
                            Token(
                                TokenType.FIN_SENTENCIA,
                                "::"
                            )
                        )
                        continue

                    raise LexicalError(
                        "Se esperaba ':'"
                    )

                raise LexicalError(
                    f"Símbolo inválido: {self.current}"
                )

            tokens.append(
                Token(
                    TokenType.EOF,
                    "EOF"
                )
            )

            return tokens
    
    # Reconocer caracteres
    def character(self):

        self.advance()

        if self.current is None:
            raise LexicalError(
                "Carácter inválido."
            )

        lexema = self.current
        self.advance()

        if self.current != "'":
            raise LexicalError(
                "Carácter inválido."
            )

        self.advance()

        return Token(
            TokenType.CARACTER,
            lexema
        )

    # Comentarios de línea
    def peek(self):
        next_position = self.position + 1

        if next_position >= len(self.source):
            return None
        
        return self.source[next_position]
    
    # Comentario en línea
    def skip_line_comment(self):
      while (self.current is not None and self.current != "\n"):
          self.advance()

    # Comentarios en bloque
    def skip_block_comment(self):

        self.advance()
        self.advance()

        while self.current is not None:
            if (
                self.current == "*"
                and self.peek() == "/"
            ):
                self.advance()
                self.advance()
                return
            
            self.advance()

        raise LexicalError("Comentario de bloque sin cerrar.")