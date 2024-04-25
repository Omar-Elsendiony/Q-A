############ essential imports ###########
import unittest
import sys
import path
#########################################
########################################
import warnings

import unittest.test
warnings.filterwarnings("ignore")
########################################

# directory reach
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from operators import *
import utils
# import unparseAST
from ast import List


class TestBase(unittest.TestCase):
        def utility_2(self, line: str, expected_results: List):
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

            numberMutationsNeeded = 17
            for m in range(numberMutationsNeeded):
                for f in faultyLineLocations:
                    tokenList, tokenSet, offsets = utils.segmentLine(splitted_cand[f])
                    op_f_list, op_f_weights = utils.mutationsCanBeApplied(tokenSet)
                    if (op_f_list == []):
                        continue
                    choice = (random.choices(op_f_list, weights=op_f_weights, k=1)[0])
                    # start mutation
                    op = name_to_operator[choice]
                    copied_line_ast = self.copier.visit(line_ast)
                    copied_line_ast.type_ignores = []
                    mutant = op(target_node_lineno = f + 1, code_ast = line_ast).visitC()
                    mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
                    line_ast = copied_line_ast
                    res = (ast.unparse(mutant))
                    mutationsDone.append(res)
                    # print("------------------")
                    # print(res)
                    # print("------------------")
            for m in mutationsDone:
                print("*******************************************")
                # print(m)
                # print(expected_results[0])
                print("*******************************************")
                if mutationsDone in expected_results:
                    print("Mutation is correct")
                    break