from source_code import *

def test_0():
    pass
    input_0 = [3, 4, 5, 5, 5, 5, 6]
    input_1 = 5
    assert find_first_in_sorted(input_0, input_1) == 2

def test_1():
    pass
    input_0 = [3, 4, 5, 5, 5, 5, 6]
    input_1 = 7
    assert find_first_in_sorted(input_0, input_1) == -1

def test_2():
    pass
    input_0 = [3, 4, 5, 5, 5, 5, 6]
    input_1 = 2
    assert find_first_in_sorted(input_0, input_1) == -1

def test_3():
    pass
    input_0 = [3, 6, 7, 9, 9, 10, 14, 27]
    input_1 = 14
    assert find_first_in_sorted(input_0, input_1) == 6