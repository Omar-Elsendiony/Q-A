from __init__ import *

class TestLoop(TestBase):

    def test_slice(self):
        """
        Testing reverse iteration loop
        """

        line = """
d = [1, 2, 3, 4, 5, 6, 7, 8, 9]
if (val is none):
    c = d[1:9]
        """
        self.utility_2(line, ["""
if (val is not None):
    a = b[1:9]
        """])




if __name__ == '__main__':
    unittest.main()