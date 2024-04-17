from ast import List
from __init__ import *
import time
import re

class TestLogical(unittest.TestCase):
    def setUp(self) -> None:
        warnings.filterwarnings("ignore")
        self.copier = copyAST.copyMutation()
    
    def getNameToOperatorMap(self):
        name_to_operator = utils.build_name_to_operator_map()
        return name_to_operator

    def test_regex(self):
        """
        Testing regex
        """
        start = time.time()
        line = "s = 1 + 2"
        line = re.sub(r'\+', r'-', line)
        span = time.time() - start
        print(span)
        print(line)

    def test_ast(self):
        """
        Testing regex
        """
        start = time.time()
        line = "s = 1 + 2"
        line = re.sub(r'\+', r'-', line)
        span = time.time() - start
        print(span)
        print(line)


if __name__ == '__main__':
    unittest.main()





if __name__ == '__main__':
    unittest.main()