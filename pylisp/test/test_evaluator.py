from pylisp import evaluator as e
from pylisp import environment as env
from pylisp import parser as p
from nose.tools import raises


class TestEvaluator:
    def setup(self):
        pass

    def test_symbol(self):
        raise NotImplementedError

    def test_non_symbol_atom(self):
        assert e.eval(3) == 3
        assert e.eval(3.14159) == 3.14159
        assert e.eval('test_string') == 'test_string'
        assert e.eval(True) == True
        assert e.eval(False) == False

    def test_quote(self):
        quote = ['quote', ['+', 3, 3]]
        assert e.eval(quote) == ['+', 3, 3]

    def test_if(self):
        true_if_statement = [p._if, [p.Symbol('='), 1, 1], 5, 'blah']
        false_if_statement = [p._if, [p.Symbol('='), 1, 2], 5, 'blah']
        assert e.eval(true_if_statement) == 5
        assert e.eval(false_if_statement) == 'blah'

    def test_define(self):
        e.eval([p._define, p.Symbol('x'), 3])
        assert e.eval(p.Symbol('x')) == 3

    def test_lambda(self):
        lambda_list = [p._lambda, p.Symbol('x'),
                        [p.Symbol('+'), p.Symbol('x'), p.Symbol('x')]]
        lambda_func = e.eval(lambda_list)
        assert type(lambda_func) == type(e.Procedure('blah', 'blah', 'blah'))
        assert lambda_func(3) == 6

    def test_set(self):
        e.eval([p._set, p.Symbol('x'), 3])
        assert e.eval(p.Symbol('x')) == 3

    def test_begin(self):
        set_var = e.eval([p._begin,
                          [p._define, p.Symbol('x'), 3],
                          [p._set, p.Symbol('x'), 5],
                          [p.Symbol('+'), p.Symbol('x'), 1]])
        assert set_var == 6
