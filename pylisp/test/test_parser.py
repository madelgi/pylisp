from pylisp import parser
from nose.tools import raises


class TestParser:
    def setup(self):
        self.input_str = "(if (= 1 (+ 0 1)) (print 1.111) (+ 3 4))"
        self.tokenized = [
                '(', 'if',
                    '(', '=', '1',
                        '(','+', '0', '1', ')', ')',
                    '(', 'print', '1.111', ')',
                    '(', '+', '3', '4', ')', ')'
                ]
        self.parsed = [
                'if',
                    ['=', 1,
                        ['+', 0, 1]],
                    ['print', 1.111],
                    ['+', 3, 4]]

    def test_parse(self):
        assert parser.parse(self.input_str) == self.parsed

    def test_tokenize(self):
        assert parser.tokenize(self.input_str) == self.tokenized

    def test_read_from_tokens(self):
        assert parser.read_from_tokens(self.tokenized) == self.parsed

    @raises(SyntaxError)
    def test_read_from_tokens_eof_exception(self):
        parser.read_from_tokens([])

    @raises(SyntaxError)
    def test_read_from_tokens_unbalanced_parens(self):
        parser.read_from_tokens([')'])

    def test_atom_int(self):
        assert parser.atom('3') == 3

    def test_atom_float(self):
        assert parser.atom('3.14') == 3.14

    def test_atom_str(self):
        assert parser.atom('hello') == 'hello'
