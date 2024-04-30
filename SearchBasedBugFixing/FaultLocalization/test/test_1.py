from src import *

def add(a, b, c = None):
    return a + b

def test_add():
    assert calculator('+',2,3) == 5


def test_sub():
    assert calculator('-',2,3) == -1

from src import *

def test_0():
    pass
    inputs = (1, 2)
    assert add(*inputs) == 3

def test_1():
    pass
    inputs = (3, 4)
    assert add(*inputs) == 7

def test_2():
    pass
    inputs = (5, 6, [1, 2])
    assert add(*inputs) == 11