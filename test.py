
# def parse_exec_res(runResult):
#   errors = []
#   isErrorBlock = False
#   i = 0
#   while i < len(runResult):
#     errorInst = ""
#     isErrorBlock = False
#     while (runResult[i] == "="):
#       isErrorBlock = True
#       i += 1
#     if (isErrorBlock):
#         while (runResult[i] != "="):
#             errorInst += runResult[i]
#             i += 1
#         errors.append(errorInst)
#     i += 1
#   return errors


# error = """
# ..F.....F
# ======================================================================
# FAIL: test_multiple_brackets_no_nesting (__main__.TestIsNested)
# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "<string>", line 38, in test_multiple_brackets_no_nesting
# AssertionError: True is not false

# ======================================================================
# FAIL: test_unmatched_brackets (__main__.TestIsNested)
# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "<string>", line 50, in test_unmatched_brackets
# AssertionError: True is not false

# ----------------------------------------------------------------------
# Ran 9 tests in 0.000s

# FAILED (failures=2)
# """

# res = parse_exec_res(error)
# print(len(res))

# for i in res:
#    print(i)