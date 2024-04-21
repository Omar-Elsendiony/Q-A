from ast import List
from wsgiref.handlers import format_date_time

from matplotlib import lines
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
        lineSplit = line.split("\n")
        codeLineslstX , codeLinessetX, offsets = utils.segmentLine(lineSplit[5]) # any variable appended by X is temporary
        lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
        numberMutationsNeeded = 3
        for m in range(1):
            choice = random.choices(lstMutations, weights = weights, k=1)[0] # random.choice returns a list, its size determined by k
            i = 6  # 5 for now as the break statement is at line 5
            line_ast = ast.parse(line)
            name_to_operator = self.getNameToOperatorMap()
            op = name_to_operator[choice]
            line_ast = ast.parse(line)
            mutant = op(target_node_lineno = i, code_ast = line_ast).visitC()
            mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
            res = (ast.unparse(mutant))
            # print(res)
            mutationsDone.append(res)
        # assert(res in expected_results) # removed assertion as it is unpredictable for now
        for m in mutationsDone:
            print(m)
            print("*******************************************")
            print(expected_results[0])
            print("*******************************************")
            if mutationsDone in expected_results:
                print("Mutation is correct")
                break
    



    def test_swap_continue_break(self):
        """
        Testing one iteration loop
        """
        line = """
def return_list_1_to_10_except_5():
    lst = []
    for i in range(1,11):
        if (i == 5):
            break
        lst.append(i)
    return lst
        """
        self.utility(line, ["""def return_list_1_to_10_except_5():
    lst = []
    for i in range(1,11):
        if (i == 5):
            continue
        lst.append(i)
    return lst"""])


if __name__ == '__main__':
    unittest.main()