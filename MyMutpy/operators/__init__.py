from .arithmetic import *
from .copyAST import *
from .logical import *



standard_operators = {
    ArithmeticOperatorDeletion,
    BinaryOperatorReplacement,
    MultiplicationOperatorReplacement,
    DivisionOperatorReplacement,
    ModuloOperatorReplacement,
    PowerOperatorReplacement,
    FloorDivisionOperatorReplacement,
    # UnaryOperatorReplacement,

}

experimental_operators = set()


# validOperation = {
#     'Add', 
#     'Sub', 
#     'Mult', 
#     'Div', 
#     'Mod', 
#     'Pow', 
#     'LShift',
#     'RShift', 
#     'BitOr', 
#     'BitXor', 
#     'BitAnd', 
#     'FloorDiv'
# }

