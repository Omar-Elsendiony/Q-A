from __init__ import *

class TestLoop(TestBase):

    def test_is(self):
        """
        Testing reverse iteration loop
        """

        line = """
if (val is none):
    print('None')
        """
        self.utility_2(line, ["""
if (val is not None):
    print('None')
        """])


#     def test_is_not(self):
#         """
#         Testing one iteration loop
#         """
#         line = """
# if (val is not None):
#     print('is not None')
#         """
#         self.utility_2(line, ["""
# if (val is None):
#     print('is not None')
#         """])

#     def test_in(self):
#         """
#         Testing delete loop
#         """
#         line = """
# x = 2
# for i in range(10):
#     print(i)
#         """
#         self.utility_2(line, ["""
# x = 2
#         """])


if __name__ == '__main__':
    unittest.main()