from pylisp import parser as p
from nose.tools import raises


class TestParser:
    def setup(self):
        self.input_str = "(if (= 1 (+ 0 1)) (print 1.111) (+ 3 4))"
        self.parsed = [
                'if',
                    ['=', 1,
                        ['+', 0, 1]],
                    ['print', 1.111],
                    ['+', 3, 4]]

    def test_parse(self):
        assert p.parse(self.input_str) == self.parsed

    def test_atom_int(self):
        assert p.atom('3') == 3

    def test_atom_float(self):
        assert p.atom('3.14') == 3.14

    def test_atom_str(self):
        assert p.atom('hello') == 'hello'
