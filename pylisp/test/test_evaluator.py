from pylisp import evaluator, parser
from nose.tools import raises


class TestEvaluator:
    def setup(self):
        pass

    def test_eval_symbol(self):
        pass

    def test_eval_list(self):
        pass

    def test_eval_quote(self):
        quote = ['quote', ['+', 3, 3]]
        assert evaluator.eval(quote) == ['+', 3, 3]

    def test_eval_if(self):
        true_if_statement = ['if', ['=', 1, 1], 5, 'blah']
        false_if_statement = ['if', ['=', 1, 2], 5, 'blah']
        assert evaluator.eval(true_if_statement) == 5
        assert evaluator.eval(false_if_statement) == 'blah'

    def test_eval_define(self):
        pass
