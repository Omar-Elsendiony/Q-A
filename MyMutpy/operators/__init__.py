from .arithmetic import *
from .copyAST import *
from .logical import *
from .conditional import *
from .loop import *


standard_operators = {
    ArithmeticOperatorDeletion,
    AdditionOperatorReplacement,
    SubtractionOperatorReplacement,
    MultiplicationOperatorReplacement,
    DivisionOperatorReplacement,
    ModuloOperatorReplacement,
    PowerOperatorReplacement,
    FloorDivisionOperatorReplacement,
    UnaryOperatorDeletion,
    LogicalOperatorReplacement,
    RelationalOperatorReplacement,
    BitwiseOperatorReplacement,
    ConditionalOperatorInsertion,
    OneIterationLoop,
    ZeroIterationLoop,
    ReverseIterationLoop
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

