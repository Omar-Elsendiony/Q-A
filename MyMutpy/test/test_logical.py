from __init__ import *

class TestLogical(unittest.TestCase):
    def setUp(self) -> None:
        warnings.filterwarnings("ignore")
        self.copier = copyAST.copyMutation()
    
    def getNameToOperatorMap(self):
        name_to_operator = utils.build_name_to_operator_map()
        return name_to_operator

    def test_GT(self):
        """
        Testing greater than operator
        Checking the result conforms with the expected results
        """
        line = "GT = 1 > 2"
        expected_results = ["GT = 1 < 2", "GT = 1 >= 2"]
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
        res = (unparseAST.to_source(mutant))
        print(res)
        assert(res in expected_results)

    def test_LT(self):
        """
        Testing greater than operator
        Checking the result conforms with the expected results
        """
        line = "GT = 1 < 2"
        expected_results = ["GT = 1 <= 2", "GT = 1 > 2"]
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
        res = (unparseAST.to_source(mutant))
        print(res)
        assert(res in expected_results)

    def test_LtE(self):
        """
        Testing greater than operator
        Checking the result conforms with the expected results
        """
        line = "GT = 1 <= 2"
        expected_results = ["GT = 1 < 2", "GT = 1 >= 2"]
        codeLineslstX , codeLinessetX, offsets = utils.segmentLine(line)
        lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
        choice = random.choices(lstMutations, weights = weights, k=1)[0]
        i = 1
        line_ast = ast.parse(line)
        name_to_operator = self.getNameToOperatorMap()
        op = name_to_operator[choice]
        lineParsedOriginal = self.copier.visit(line_ast)
        line_ast = ast.parse(line)
        mutant = op(target_node_lineno = i, code_ast = line_ast).visitC()
        mutant = ast.fix_missing_locations(mutant)
        res = (unparseAST.to_source(mutant))
        # print(res)
        assert(res in expected_results)





    def test_division(self):
        pass

if __name__ == '__main__':
    unittest.main()