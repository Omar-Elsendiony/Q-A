from __init__ import *

class TestArithmetic(unittest.TestCase):
    def setUp(self) -> None:
        warnings.filterwarnings("ignore")

        # self.op = ArithmeticOperatorDeletion()
        self.copier = copyAST.copyMutation()
    
    def getNameToOperatorMap(self):
        name_to_operator = utils.build_name_to_operator_map()
        return name_to_operator

    def test_addition(self):
        """
        testing the mutation of the addition operator by replacing the addition operator with the subtraction operator
        """
        line = "sum = 1 + 2"
        codeLineslstX , codeLinessetX, offsets = utils.segmentLine(line) # any variable appended by X is temporary
        # assume know we are going to mutate the code line by line
        # print(len(codeLineslstX), len(codeLinessetX), len(offsets))
        # print(codeLineslstX)
        # print(offsets)
        lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
        choice = random.choices(lstMutations, weights = weights, k=1)[0] # random.choice returns a list, its size determined by k
        i = 1
        line_ast = ast.parse(line)
        name_to_operator = self.getNameToOperatorMap()
        if (type(choice) is tuple):
            opCode = choice[0]
            operator = choice[1]
            op = name_to_operator[opCode]
            lineParsedOriginal = self.copier.visit(line_ast)
            mutant = op(target_node_lineno = i, code_ast = line_ast, operator = operator).visitC()
            mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
            # print("**********************************")
            res = (unparseAST.to_source(mutant))
            assert(res == "sum = 1 - 2")
            # print("**********************************")
        else:
            op = name_to_operator[choice]
            lineParsedOriginal = self.copier.visit(line_ast)
            line_ast = ast.parse(line)
            mutant = op(target_node_lineno = i, code_ast = line_ast).visitC()
            mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations

    def test_subtraction(self):
        """
        Testing mutation of the subtraction operator
        The result should be the replacement of the subtraction operator with the addition operator
        """
        line = "diff = 1 - 2"
        codeLineslstX , codeLinessetX, offsets = utils.segmentLine(line) # any variable appended by X is temporary
        # assume know we are going to mutate the code line by line
        # print(len(codeLineslstX), len(codeLinessetX), len(offsets))
        # print(codeLineslstX)
        # print(offsets)
        lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
        choice = random.choices(lstMutations, weights = weights, k=1)[0] # random.choice returns a list, its size determined by k
        i = 1
        line_ast = ast.parse(line)
        name_to_operator = self.getNameToOperatorMap()
        if (type(choice) is tuple):
            opCode = choice[0]
            operator = choice[1]
            op = name_to_operator[opCode]
            lineParsedOriginal = self.copier.visit(line_ast)
            mutant = op(target_node_lineno = i, code_ast = line_ast, operator = operator).visitC()
            mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
            # print("**********************************")
            res = (unparseAST.to_source(mutant))
            assert(res == "diff = 1 + 2")
            # print("**********************************")

    def test_multiplication(self):
        """
        Testing mutation of the subtraction operator
        The result should be the replacement of the subtraction operator with the addition operator
        """
        line = "mult = 1 * 2"
        expected_results = ["mult = 1 / 2", "mult = 1 ** 2"]
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
        # print(res)
        assert(res in expected_results)


    def test_division(self):
        pass

if __name__ == '__main__':
    unittest.main()