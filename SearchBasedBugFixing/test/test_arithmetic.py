from ast import List
from __init__ import *

class TestArithmetic(TestBase):

    # def utility(self, line: str, expected_results: List):
    #     codeLineslstX , codeLinessetX, offsets = utils.segmentLine(line) # any variable appended by X is temporary
    #     lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
    #     choice = random.choices(lstMutations, weights = weights, k=1)[0] # random.choice returns a list, its size determined by k
    #     i = 1
    #     line_ast = ast.parse(line)
    #     name_to_operator = self.getNameToOperatorMap()
    #     op = name_to_operator[choice]
    #     mutant = op(target_node_lineno = i, code_ast = line_ast).visitC()
    #     # mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
    #     res = (ast.unparse(mutant))
    #     print(res)
    #     assert(res in expected_results)

    # def test_addition(self):
    #     """
    #     testing the mutation of the addition operator by replacing the addition operator with the subtraction operator
    #     """
    #     line = "sum = 1 + 2"
    #     expected_results = ["sum = 1 - 2", "sum = 1 * 2", "sum = 1 / 2"]
    #     self.utility_2(line, expected_results)

    # def test_subtraction(self):
    #     """
    #     Testing mutation of the subtraction operator
    #     The result should be the replacement of the subtraction operator with the addition operator
    #     """
    #     line = "diff = 1 - 2"
    #     expected_results = ["diff = 1 + 2", "diff = 1 * 2", "diff = 1 / 2"]
    #     self.utility_2(line, expected_results)


    # def test_multiplication(self):
    #     """
    #     Testing mutation of the subtraction operator
    #     The result should be the replacement of the subtraction operator with the addition operator
    #     """
    #     line = "mult = 1 * 2"
    #     expected_results = ["mult = 1 / 2", "mult = 1 ** 2"]
    #     self.utility_2(line, expected_results)


    def test_division(self):
        """
        Testing mutation of the subtraction operator
        The result should be the replacement of the subtraction operator with the addition operator
        """
        line = "div = 1 ** 2 ** 3"
        expected_results = ["div = 1 * 2", "div = 1 ** 2"]
        self.utility_2(line, expected_results)

    # def test_remove_binary_op(self):
    #     """
    #     Testing mutation of the subtraction operator
    #     The result should be the replacement of the subtraction operator with the addition operator
    #     """
    #     line = "average = total_sum / (len(numbers) - 1)  # This is incorrect"
    #     expected_results = ["average = total_sum / (len(numbers))"]
    #     self.utility_2(line, expected_results)

if __name__ == '__main__':
    unittest.main()
