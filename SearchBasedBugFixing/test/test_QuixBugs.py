import unittest
from __init__ import *


class TestQuix(TestBase): # type: ignore

    def test_lcs(self):
        """
        Testing one iteration loop
        """
        line = """
dp[i, j] = dp[i - 1, j] + 1
        """
        self.utility_2(line, ["""dp[i, j] = dp[i - 1, j - 1] + 1 if i > 0 and j > 0 else 1"""])
    
#     def test_leveshtein(self):
#         line = """
# return levenshtein(source[1:], target[1:])
# """
#         self.utility_2(line, [""""""])

#     def test_mergeSort(self):
#         line = """
# if len(arr) == 0:
#         return arr
#         """
#         self.utility_2(line, [""""""])
        
#     def test_bucketSort(self):
#         line = """
# for i, count in enumerate(arr, arr2): pass
#         """
#         self.utility_2(line, [""""""])
    
#     def test_yield(self):
#         line = """
# for i, count in enumerate(arr, x): pass
#         """
#         self.utility_2(line, [""""""])

    # def test_yield(self):
    #     line = """steps = []; steps.append((start, helper))"""
    #     self.utility_2(line, [""""""])   
    
    def test_ret(self):
        line = """return min(
levenshtein(source,     target[1:]),
levenshtein(source[1:], target[1:]),
levenshtein(source[1:], target))"""
        self.utility_2(line, [""""""])
    
if __name__ == '__main__':
    unittest.main()
