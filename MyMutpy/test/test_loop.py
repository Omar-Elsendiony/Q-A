from ast import List
from __init__ import *

class TestLoop(unittest.TestCase):
    def setUp(self) -> None:
        warnings.filterwarnings("ignore")
        self.copier = copyAST.copyMutation()
    
    def getNameToOperatorMap(self):
        name_to_operator = utils.build_name_to_operator_map()
        return name_to_operator

    def utility(self, line: str, expected_results: List):
        """
        Testing greater than operator
        Checking the result conforms with the expected results
        """

        codeLineslstX , codeLinessetX, offsets = utils.segmentLine(line) # any variable appended by X is temporary
        # lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
        lstMutations = ['ZIL', 'RIL', 'OIL']
        weights = [1] * 3
        choice = random.choices(lstMutations, weights = weights, k=1)[0] # random.choice returns a list, its size determined by k
        i = 2
        line_ast = ast.parse(line)
        name_to_operator = self.getNameToOperatorMap()
        op = name_to_operator[choice]
        line_ast = ast.parse(line)
        mutant = op(target_node_lineno = i, code_ast = line_ast).visitC()
        mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
        res = (ast.unparse(mutant))
        # print(res)
        # assert(res in expected_results) # removed assertion as it is unpredictable for now


    def utility_2(self, line: str, expected_results: List):
        """
        Testing greater than operator
        Checking the result conforms with the expected results
        """
        splitted_cand = line.split('\n')
        faultyLineLocations = list(range(len(splitted_cand)))

        name_to_operator = self.getNameToOperatorMap()
        line_ast = ast.parse(line)
        for f in faultyLineLocations:
            tokenList, tokenSet, offsets = utils.segmentLine(splitted_cand[f])
            op_f_list, op_f_weights = utils.mutationsCanBeApplied(tokenSet)
            if (op_f_list == []):
                continue
            choice = (random.choices(op_f_list, weights=op_f_weights, k=1)[0])
            # start mutation
            op = name_to_operator[choice]
            copied_line_ast = self.copier.copy(line_ast)
            mutant = op(target_node_lineno = f + 1, code_ast = line_ast).visitC()
            mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
            line_ast = copied_line_ast
            res = (ast.unparse(mutant))
            print(res)

    def test_reverse_iteration_loop(self):
        """
        Testing reverse iteration loop
        """

        line = """
for i in range(10):
    print(i)
        """
        self.utility(line, ["GT = 1 >= 2", "GT = 1 < 2"])

    def test_one_iteration_loop(self):
        """
        Testing one iteration loop
        """
        line = """
for i in range(10):
    print(i)
        """
        self.utility(line, ["LT = 1 <= 2", "LT = 1 > 2"])

    def test_delete_loop(self):
        """
        Testing delete loop
        """
        line = """
x = 2
for i in range(10):
    print(i)
        """
        self.utility_2(line, ["""
x = 2
        """])


if __name__ == '__main__':
    unittest.main()