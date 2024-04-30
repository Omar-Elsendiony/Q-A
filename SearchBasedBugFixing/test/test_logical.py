from ast import List
from __init__ import *

class TestLogical(unittest.TestCase):
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
        lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
        choice = random.choices(lstMutations, weights = weights, k=1)[0] # random.choice returns a list, its size determined by k
        i = 1
        line_ast = ast.parse(line)
        name_to_operator = self.getNameToOperatorMap()
        op = name_to_operator[choice]
        lineParsedOriginal = self.copier.visit(line_ast)
        line_ast = ast.parse(line)
        mutant = op(target_node_lineno = i, code_ast = line_ast).visitC()
        mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
        # res = unparseAST.to_source(mutant)
        # print(res)
        res = (ast.unparse(mutant))
        print(res)
        assert(res in expected_results)
    

    def test_GT(self):
        """
        Testing greater than operator
        """
        self.utility("GT = 1 > 2", ["GT = 1 >= 2", "GT = 1 < 2"])

    def test_LT(self):
        """
        Testing less than operator
        """
        self.utility("LT = 1 < 2", ["LT = 1 <= 2", "LT = 1 > 2"])

    def test_LtE(self):
        """
        Testing greater than operator
        Checking the result conforms with the expected results
        """
        self.utility("LtE = 1 <= 2", ["LtE = 1 < 2", "LtE = 1 >= 2"])


    def test_and(self):
        """
        Testing AND operator
        """
        self.utility("AND = 1 and 2", ["AND = 1 or 2"])
    
    def test_or(self):
        """
        Testing OR operator
        """
        self.utility("OR = 1 or 2", ["OR = 1 and 2"])

    def test_bitwise_or(self):
        """
        Testing bitwise OR operator
        """
        self.utility("OR = 1 | 2", ["OR = 1 & 2"])

    def test_bitwise_and(self):
        """
        Testing bitwise AND operator
        """
        self.utility("AND = 1 & 2", ["AND = 1 | 2"])
    
    def test_not(self):
        """
        Testing NOT operator
        """
        self.utility("NOT = not 1", ["NOT = 1"])


if __name__ == '__main__':
    unittest.main()