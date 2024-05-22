from source_code import *

def test_0():
    pass
    input_0 = []
    assert mergesort(input_0) == []

def test_1():
    pass
    input_0 = [1, 2, 6, 72, 7, 33, 4]
    assert mergesort(input_0) == [1, 2, 4, 6, 7, 33, 72]

def test_2():
    pass
    input_0 = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3]
    assert mergesort(input_0) == [1, 1, 2, 3, 3, 3, 4, 5, 5, 5, 6, 7, 8, 9, 9, 9]

def test_3():
    pass
    input_0 = [5, 4, 3, 2, 1]
    assert mergesort(input_0) == [1, 2, 3, 4, 5]

def test_4():
    pass
    input_0 = [5, 4, 3, 1, 2]
    assert mergesort(input_0) == [1, 2, 3, 4, 5]