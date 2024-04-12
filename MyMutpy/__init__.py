import base
import ast
from operators import *
import operators
import astunparse

validOperation = ['Add', 'Sub', 'Mult', 'Div', 'Mod', 'Pow', 'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd', 'FloorDiv']


def build_name_to_operator_map():
    result = {}
    for operator in operators.standard_operators | operators.experimental_operators:
        result[operator.name()] = operator
        # result[operator.long_name()] = operator
    return result



code = """s = 1 + 2;
s = 1 + 2"""
ast_node = ast.parse(code)
mutant = (ArithmeticOperatorReplacement(target_node_lineno= 1, code = ast_node)).visitC()
mutant = ast.fix_missing_locations(mutant)
mutant = (ArithmeticOperatorReplacement(target_node_lineno= 2, code = mutant)).visitC()
# print(ast.dump(mutant, indent=4))
print(astunparse.to_source(ast_node))


# again = ArithmeticOperatorReplacement.printMutatedSet()

res = build_name_to_operator_map()

print(res)


