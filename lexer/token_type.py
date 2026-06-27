from enum import Enum, auto


class TokenType(Enum):

    # Tipos de datos
    TIPO_INT = auto()
    TIPO_FLOAT = auto()
    TIPO_BOOL = auto()
    TIPO_STRING = auto()
    TIPO_CHAR = auto()
    TIPO_VOID = auto()

    # Entrada y salida
    PRINT = auto()
    INPUT = auto()

    # Estructuras de control
    IF = auto()
    WHILE = auto()
    ELSE = auto()
    FOR = auto()

    # Operaciones inspiradas en Assembley
    LOAD = auto()
    STORE = auto()
    MOV = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    CMP = auto()
    JUMP = auto()
    CALL = auto()
    PUSH = auto()
    POP = auto()

    # Operadores de comparación
    OP_EQ = auto()
    OP_NEQ = auto()
    OP_LT = auto() # <
    OP_GT = auto() # >
    OP_LE = auto() # <=
    OP_GE = auto() # =>

    # Literales
    ENTERO = auto()
    REAL = auto()
    CADENA = auto()
    CARACTER = auto()
    BOOLEANO = auto()

    # Identificadores y literales
    IDENTIFICADOR = auto()

    # Operadores especiales
    ASIGNACION = auto()

    # Delimitadores
    FIN_SENTENCIA = auto()
    PARENTESIS_IZQ = auto()
    PARENTESIS_DER = auto()
    LLAVE_IZQ = auto()
    LLAVE_DER = auto()
    COMA = auto()

    # Utilidades
    EOF = auto()

    