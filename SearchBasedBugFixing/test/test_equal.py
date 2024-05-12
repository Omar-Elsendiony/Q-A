from ast import List
from __init__ import *

class TestLogical(TestBase):
    

    def test_Equal(self):
        """
        Testing greater than operator
        """
        self.utility_2("weight == 2", ["GT = 1 >= 2", "GT = 1 < 2"])

    def test_NotEqual(self):
        """
        Testing greater than operator
        """
        self.utility_2("weight != 2", ["GT = 1 >= 2", "GT = 1 < 2"])


if __name__ == '__main__':
    unittest.main()
