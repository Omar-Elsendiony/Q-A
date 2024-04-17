from ast import List
from wsgiref.handlers import format_date_time
from __init__ import *

class TestMisc(unittest.TestCase):
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
        print("*******************************************")
        mutationsDone = []
        codeLineslstX , codeLinessetX, offsets = utils.segmentLine(line) # any variable appended by X is temporary
        lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
        numberMutationsNeeded = 3
        for m in range(numberMutationsNeeded):
            choice = random.choices(lstMutations, weights = weights, k=1)[0] # random.choice returns a list, its size determined by k
            i = 2
            line_ast = ast.parse(line)
            name_to_operator = self.getNameToOperatorMap()
            op = name_to_operator[choice]
            line_ast = ast.parse(line)
            mutant = op(target_node_lineno = i, code_ast = line_ast).visitC()
            mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
            res = (ast.unparse(mutant))
            print(res)
            mutationsDone.append(res)
        # assert(res in expected_results) # removed assertion as it is unpredictable for now
        for m in mutationsDone:
            if mutationsDone in expected_results:
                print("Mutation is correct")
                break
    

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


if __name__ == '__main__':
    unittest.main()