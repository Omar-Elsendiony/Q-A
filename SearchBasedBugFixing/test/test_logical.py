from ast import List
from __init__ import *

class TestLogical(TestBase):
    

    def test_GT(self):
        """
        Testing greater than operator
        """
        self.utility_2("if weight < j and loler < i:pass", ["GT = 1 >= 2", "GT = 1 < 2"])

    # def test_LT(self):
    #     """
    #     Testing less than operator
    #     """
    #     self.utility_2("LT = 1 < 2", ["LT = 1 <= 2", "LT = 1 > 2"])

    # def test_LtE(self):
    #     """
    #     Testing greater than operator
    #     Checking the result conforms with the expected results
    #     """
    #     self.utility_2("LtE = 1 <= 2", ["LtE = 1 < 2", "LtE = 1 >= 2"])


    # def test_and(self):
    #     """
    #     Testing AND operator
    #     """
    #     self.utility_2("AND = 1 and 2", ["AND = 1 or 2"])
    
    # def test_or(self):
    #     """
    #     Testing OR operator
    #     """
    #     self.utility_2("OR = 1 or 2", ["OR = 1 and 2"])

    # def test_bitwise_or(self):
    #     """
    #     Testing bitwise OR operator
    #     """
    #     self.utility_2("OR = 1 | 2", ["OR = 1 & 2"])

    # def test_bitwise_and(self):
    #     """
    #     Testing bitwise AND operator
    #     """
    #     self.utility_2("AND = 1 & 2", ["AND = 1 | 2"])
    
    # def test_not(self):
    #     """
    #     Testing NOT operator
    #     """
    #     self.utility_2("NOT = not 1", ["NOT = 1"])


if __name__ == '__main__':
    unittest.main()
