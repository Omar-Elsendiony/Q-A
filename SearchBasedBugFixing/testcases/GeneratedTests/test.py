from source_code import *

def test_0():
    pass
    input_0 = 100
    input_1 = [[60, 10], [50, 8], [20, 4], [20, 4], [8, 3], [3, 2]]
    assert knapsack(input_0, input_1) == 19

def test_1():
    pass
    input_0 = 40
    input_1 = [[30, 10], [50, 5], [10, 20], [40, 25]]
    assert knapsack(input_0, input_1) == 30

def test_2():
    pass
    input_0 = 750
    input_1 = [[70, 135], [73, 139], [77, 149], [80, 150], [82, 156], [87, 163], [90, 173], [94, 184], [98, 192], [106, 201], [110, 210], [113, 214], [115, 221], [118, 229], [120, 240]]
    assert knapsack(input_0, input_1) == 1458

def test_3():
    pass
    input_0 = 26
    input_1 = [[12, 24], [7, 13], [11, 23], [8, 15], [9, 16]]
    assert knapsack(input_0, input_1) == 51

def test_4():
    pass
    input_0 = 50
    input_1 = [[31, 70], [10, 20], [20, 39], [19, 37], [4, 7], [3, 5], [6, 10]]
    assert knapsack(input_0, input_1) == 107

def test_5():
    pass
    input_0 = 190
    input_1 = [[56, 50], [59, 50], [80, 64], [64, 46], [75, 50], [17, 5]]
    assert knapsack(input_0, input_1) == 150