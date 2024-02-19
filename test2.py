code = """def is_nested(string):
    opening_bracket_index = []
    closing_bracket_index = []
    for i in range(len(string)):
        if string[i] == "[":
            opening_bracket_index.append(i)
        else:
            closing_bracket_index.append(i)
    closing_bracket_index.reverse()
    cnt = 0
    i = 0
    l = len(closing_bracket_index)
    for idx in opening_bracket_index:
        if i < l and idx < closing_bracket_index[i]:
            cnt += 1
            i += 1
    return cnt >= 2


import unittest


class TestIsNested(unittest.TestCase):

    def setUp(self):
        self.is_nested_function = is_nested

    def test_empty_string(self):
        self.assertFalse(self.is_nested_function(""))

    def test_single_opening_bracket(self):
        self.assertFalse(self.is_nested_function("["))

    def test_single_closing_bracket(self):
        self.assertFalse(self.is_nested_function("]"))

    def test_multiple_brackets_no_nesting(self):
        self.assertFalse(self.is_nested_function("[][][][]"))

    def test_nested_brackets(self):
        self.assertTrue(self.is_nested_function("[[[]]]"))

    def test_multiple_nested_brackets(self):
        self.assertTrue(self.is_nested_function("[[[]]]][[[]]]"))

    def test_nested_brackets_with_non_nested_brackets(self):
        self.assertTrue(self.is_nested_function("[[]][[[]]]"))

    def test_unmatched_brackets(self):
        self.assertFalse(self.is_nested_function("[[[]]]]"))

    def test_consecutive_nested_brackets(self):
        self.assertTrue(self.is_nested_function("[[[][]]]"))


if __name__ == "__main__":
    unittest.main()
"""

import sys
from io import StringIO


def runCode(code):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    oldstderr = sys.stderr
    redirected_output2 = sys.stderr = StringIO()
    result = ""
    try:
        exec(code, globals())
        result = redirected_output.getvalue()
    except Exception as e:
        print(repr(e))
        result = repr(e)
    except SystemExit as s:
        print(repr(s))
        result = redirected_output2.getvalue()
    sys.stdout = old_stdout
    sys.stderr = oldstderr
    return result


# print(result)
# print(result)


# exec(code)
print(runCode(code))