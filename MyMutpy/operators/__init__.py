from .arithmetic import *
from .copyAST import *




standard_operators = {
    ArithmeticOperatorDeletion,
    BinaryOperatorReplacement,
    # AssignmentOperatorReplacement
}

experimental_operators = set()


validOperation = {
    'Add', 
    'Sub', 
    'Mult', 
    'Div', 
    'Mod', 
    'Pow', 
    'LShift',
    'RShift', 
    'BitOr', 
    'BitXor', 
    'BitAnd', 
    'FloorDiv'
}

