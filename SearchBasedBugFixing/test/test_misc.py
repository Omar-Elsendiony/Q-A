from __init__ import *

class TestMisc(TestBase):

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
        self.utility_2(line, ["""def return_list_1_to_10_except_5():
    lst = []
    for i in range(1,11):
        if (i == 5):
            continue
        lst.append(i)
    return lst"""])


if __name__ == '__main__':
    unittest.main()