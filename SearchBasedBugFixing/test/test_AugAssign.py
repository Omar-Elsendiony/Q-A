from ast import List
from __init__ import *

class TestAugAssign(TestBase):


    def test_negate_while_conditon(self):
        line = "x -= 1"
        self.utility_2(line, ["x ^= 1", "x -= 1", "x *= 1", "x /= 1", "x //= 1", "x %= 1", "x <<= 1", "x >>= 1", "x &= 1", "x |= 1", "x **= 1"])

    # def test_negate_if_condition(self):
    #     """
    #     Testing less than operator
    #     """
    #     line = "if i < 10 and l != 3: pass"  
    #     self.utility_2(line, ["if i > 10 and l == 3: pass"])

    # def test_delete_if_condition(self):
    #     """
    #     Testing less than operator
    #     """
    #     line = "if i < 10 and l != 3: pass"
    #     self.utility_2(line, ["if i > 10 and l == 3: pass"])




if __name__ == '__main__':
    unittest.main()