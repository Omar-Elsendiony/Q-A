from .arithmetic import *
from .copyAST import *
from .logical import *



standard_operators = {
    ArithmeticOperatorDeletion,
    AdditionOperatorReplacement,
    SubtractionOperatorReplacement,
    MultiplicationOperatorReplacement,
    DivisionOperatorReplacement,
    ModuloOperatorReplacement,
    PowerOperatorReplacement,
    FloorDivisionOperatorReplacement,
    # UnaryOperatorReplacement,
    LogicalOperatorReplacement,
    RelationalOperatorReplacement,
    # BitwiseOperatorReplacement,

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

