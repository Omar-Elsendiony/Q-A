from source_code import *

def test_0():
    pass
    input_0 = 'headache'
    input_1 = 'pentadactyl'
    assert longest_common_subsequence(input_0, input_1) == eadac

def test_1():
    pass
    input_0 = 'daenarys'
    input_1 = 'targaryen'
    assert longest_common_subsequence(input_0, input_1) == aary

def test_2():
    pass
    input_0 = 'XMJYAUZ'
    input_1 = 'MZJAWXU'
    assert longest_common_subsequence(input_0, input_1) == MJAU

def test_3():
    pass
    input_0 = 'thisisatest'
    input_1 = 'testing123testing'
    assert longest_common_subsequence(input_0, input_1) == tsitest