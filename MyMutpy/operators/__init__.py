from .arithmetic import *
from .copyAST import *
from .logical import *
from .conditional import *
from .loop import *
from .misc import *



standard_operators = {
    ## ARITHMETIC ##
    ArithmeticOperatorDeletion,
    AdditionOperatorReplacement,
    SubtractionOperatorReplacement,
    MultiplicationOperatorReplacement,
    DivisionOperatorReplacement,
    ModuloOperatorReplacement,
    PowerOperatorReplacement,
    FloorDivisionOperatorReplacement,
    UnaryOperatorDeletion,
    ## LOGICAL ##
    LogicalOperatorReplacement,
    RelationalOperatorReplacement,
    BitwiseOperatorReplacement,
    ConditionalOperatorInsertion,
    ## LOOPS ##
    OneIterationLoop,
    ZeroIterationLoop,
    ReverseIterationLoop,
    ## MISC ##
    SliceIndexRemove,
    BreakContinueReplacement,
    StatementDeletion
}

experimental_operators = set()



