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
    AugmentedAssignReplacement,
    ## LOGICAL ##
    LogicalOperatorReplacement,
    RelationalOperatorReplacement,
    BitwiseOperatorReplacement,
    ConditionalOperatorInsertion,

    ## LOOPS ##
    OneIterationLoop,
    ZeroIterationLoop,
    ReverseIterationLoop,
    LoopDeletion,

    ## CONDITIONAL ##
    ConditionalOperatorInsertion,
    ConditionalDeletion,

    ## MISC ##
    SliceIndexRemove,
    BreakContinueReplacement,
    StatementDeletion,
    ConstantNumericReplacement,
    ConstantStringReplacement,

    ## MEMBERSHIP ##
    MembershipReplacement,

    ## ASSIGNMENT ##
    ## UNARY ##

}

experimental_operators = set()



