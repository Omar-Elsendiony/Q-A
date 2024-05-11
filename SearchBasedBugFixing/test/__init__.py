############ essential imports ###########
import unittest
import sys
import path
#########################################
########################################
import warnings
warnings.filterwarnings("ignore")
########################################
# directory reach
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
###############################################
from operators import *
import utils
from typing import List
import ast
from SearchBasedBugFixing.identifier.identifierVisitor import IdentifierVisitor
from operators.base import *


class TestBase(unittest.TestCase):
        def setUp(self) -> None:
            warnings.filterwarnings("ignore")
            self.copier = copyAST.copyMutation()
    
        def getNameToOperatorMap(self):
            name_to_operator = utils.build_name_to_operator_map()
            return name_to_operator

        def utility_2(self, line: str, expected_results: List):  # it is actually not line but a list of lines(candidates)
            """
            Testing greater than operator
            Checking the result conforms with the expected results
            """
            mutationsDone = []
            splitted_cand = line.split('\n')
            faultyLineLocations = list(range(len(splitted_cand)))
            # print(faultyLineLocations)
            name_to_operator = self.getNameToOperatorMap()
            line_ast = ast.parse(line)
            line_ast.type_ignores = []
            utils.parentify(line_ast)
            idVistitor = IdentifierVisitor()
            idVistitor.visit(line_ast)
            baseOperator.set_identifiers(list(idVistitor.get_identifiers))
            # print("------------------------------------")
            # print(baseOperator.get_identifiers())
            # print("------------------------------------")

            numberMutationsNeeded = 1
            for m in range(numberMutationsNeeded):
                for f in faultyLineLocations:
                    utils.parentify(line_ast)
                    tokenSet, units_offsets = utils.segmentLine(splitted_cand[f])
                    op_f_list, op_f_weights, original_op = utils.mutationsCanBeApplied(tokenSet)
                    if (op_f_list == []):
                        continue
                    # changed from choosing the actual element to choosing the index, as getting 
                    # the operator attributed to the mutation is not possible with index
                    choice_index = (random.choices(range(len(op_f_list)), weights = op_f_weights, k=1)[0])
                    choice = op_f_list[choice_index]
                    colOffsets = units_offsets[original_op[choice_index]]
                    col_index = random.randint(0, len(colOffsets) - 1)
                    # print(col_index)
                    op = name_to_operator[choice]
                    copied_line_ast = self.copier.visit(line_ast)
                    copied_line_ast.type_ignores = []
                    ast.fix_missing_locations(line_ast)
                    col_index = col_index if choice != "ARD" else choice_index // 2
                    mutant = op(target_node_lineno = f + 1, indexMutation = col_index, code_ast = line_ast, specifiedOperator=original_op[choice_index]).visitC()
                    mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
                    line_ast = copied_line_ast
                    # res = (SearchBasedBugFixing.unparser.unparser().visit(mutant))
                    res = ast.unparse(mutant)
                    mutationsDone.append(res)
                    # print("------------------")
                    # print(res)
                    # print("------------------")
            for m in mutationsDone:
                print("*******************************************")
                print(m)
                # print(expected_results[0])
                print("*******************************************")
                if mutationsDone in expected_results:
                    print("Mutation is correct")
                    break
            # print("Mutation is incorrect")
