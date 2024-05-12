from ast import List
from __init__ import *

class TestConstant(TestBase):
    
        # def test_constant_plus_one(self):
        #     """
        #     Testing greater than operator
        #     """
        #     line = "return n * factorial(n)"
        #     self.utility_2(line, ["if i == 11: pass"])

    
        def test_constant_minus_one(self):
            """
            Testing greater than operator
            """
            line = "return n * factorial(n, a, l - 1)"
            self.utility_2(line, ["if i == 9: pass"])
        
        

        # def test_Str_Empty(self):
        #     """
        #     Testing less than operator
        #     """
        #     line = "x = 'what have I done'"  
        #     self.utility_2(line, ["x = ''"])
    
        # def test_delete_if_condition(self):
        #     """
        #     Testing less than operator
        #     """
        #     line = "if i < 10 and l != 3: pass"  
        #     self.utility_2(line, ["if i > 10 and l == 3: pass"])


if __name__ == '__main__':
    unittest.main()
