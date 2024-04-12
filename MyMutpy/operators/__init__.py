from .arithmetic import *





standard_operators = {
    ArithmeticOperatorDeletion,
    ArithmeticOperatorReplacement,
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

