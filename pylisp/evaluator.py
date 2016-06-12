import pylisp.parser as p
from pylisp.environment import global_env, Env


class Procedure(object):
    def __init__(self, parms, body, env):
        """A user-defined Scheme procedure.

        Args:
            parms
            body
            env

        Returns:
            A Procedure.
        """
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))


def eval(exp, env=global_env):
    """Evaluate an expression given an environment.

    Args:
        exp (scheme expression): Either a Symbol, Number, String, or List
            (representing an expression).
        env (dict): A mapping of scheme functions/vars/expressions to equivalent
            python expressions.

    Returns:
        A scheme value.

    Example:
        >>> eval(['/', 3, 3])
        1
        >>> eval(['if', ['=', 3, 3], ['quote', 'true!!!'], ['quote', -10]])
        'true!!!'

    """
    while True:
        if isinstance(exp, p.Symbol):
            return env.find(exp)[exp]
        elif not isinstance(exp, p.List):
            return exp
        elif exp[0] == p._quote:
            (_, literal) = exp
            return literal
        elif exp[0] == p._if:
            (_, test, conseq, alt) = exp
            exp = (conseq if eval(test, env) else alt)
        elif exp[0] == p._set:
            (_, var, expression) = exp
            env.find(var)[var] = eval(expression, env)
            return None
        elif exp[0] == p._define:
            (_, var, assignment) = exp
            env[var] = eval(assignment, env)
            return None
        elif exp[0] == p._lambda:
            (_, parms, body) = exp
            return Procedure(parms, body, env)
        elif exp[0] is p._begin:
            for expression in exp[1:-1]:
                eval(expression, env)
            exp = exp[-1]
        else:
            exps = [eval(x, env) for x in exp]
            proc = exps.pop(0)
            if isinstance(proc, Procedure):
                exp = proc.body
                env = Env(proc.parms, exps, proc.env)
            else:
                return proc(*exps)
