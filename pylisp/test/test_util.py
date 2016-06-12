from pylisp import util as u
from pylisp import parser as p


def test_to_string():
    assert u.to_string(True) == '#t'
    assert u.to_string(False) == '#f'
    assert u.to_string(p.Symbol('x')) == 'x'
    assert u.to_string([1, 2, 3, 4]) == '(1 2 3 4)'
    assert u.to_string(complex(4,-3)) == '(4-3i)'
