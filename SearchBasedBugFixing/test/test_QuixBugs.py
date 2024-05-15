from __init__ import *


class TestMisc(TestBase):

#     def test_lcs(self):
#         """
#         Testing one iteration loop
#         """
#         line = """
# dp[i, j] = dp[i - 1, j] + 1
#         """
#         self.utility_2(line, ["""dp[i, j] = dp[i - 1, j - 1] + 1 if i > 0 and j > 0 else 1"""])
    
    def test_leveshtein(self):
        line = """
return
        """
        self.utility_2(line, ["""dp[i, j] = dp[i - 1, j - 1] + 1 if i > 0 and j > 0 else 1"""])

    def test_mergeSort(self):
        line = """
if len(arr) == 0:
        return arr
        """
        self.utility_2(line, ["""dp[i, j] = dp[i - 1, j - 1] + 1 if i > 0 and j > 0 else 1"""])
if __name__ == '__main__':
    unittest.main()
