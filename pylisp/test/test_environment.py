from pylisp import evaluator as e
from pylisp import parser as p


class TestEnvironment:
    def setup(self):
        self.arithmetic_ops = [
            (['+', 4, 2], 6),  (['-', 3, 10], -7), (['*', 6, 4], 24),
            (['/', 10, 2], 5),
        ]
        self.logic_ops = [
            (['>', 5, 3], True),      (['<', 5, 3], False),  (['>=', 5, 5], True),
            (['<=', 5, 3], False),    (['=', 10, 10], True), (['number?', 3], True),
            (['number?', -10], True), (['number?', 3.14], True),
        ]

    def test_arithmetic_ops(self):
        for operation in self.arithmetic_ops:
            debug_str = str(operation[0]) + ' is ' + str(operation[1])
            assert e.eval(operation[0]) == operation[1], debug_str

    def test_logic_ops(self):
        for operation in self.logic_ops:
            debug_str = str(operation[0]) + ' is ' + str(operation[1])
            assert e.eval(operation[0]) == operation[1], debug_str

    def test_if_statements(self):
        pass
