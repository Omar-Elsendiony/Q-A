from ast import List

from cv2 import line
from __init__ import *

class TestConditional(unittest.TestCase):
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
        # assert(res in expected_results)
    

    def test_negate_while_conditon(self):
        """
        Testing greater than operator
        """
        line = "while i == 10: pass"
        self.utility(line, ["GT = 1 >= 2", "GT = 1 < 2"])

    def test_negate_if_condition(self):
        """
        Testing less than operator
        """
        line = "if i < 10 and l != 3: pass"  
        self.utility(line, ["LT = 1 <= 2", "LT = 1 > 2"])







if __name__ == '__main__':
    unittest.main()