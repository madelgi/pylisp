import pylisp.parser as p


class Env(dict):
    """An environment: a dict of {'var': val} pairs, with an outer Env.
    """
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """Find the innermost Env where var appears.
        """
        if var in self:
            return self
        else:
            return self.outer.find(var)


class Procedure(object):
    """A user-defined Scheme procedure.
    """
    def __init__(self, parms, body, env):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))


def standard_env():
    """TODO
    """
    import math
    import operator as op
    env = Env()
    env.update(vars(math))
    env.update({
        '+':  op.add, '-':  op.sub, '*': op.mul,
        '/':  op.div, '>':  op.gt,  '<': op.lt,
        '>=': op.ge,  '<=': op.le,  '=': op.eq,
        'abs':          abs,
        'append':       op.add,
        'apply':        apply,
        'begin':        lambda *x: x[-1],
        'car':          lambda x: x[0],
        'cdr':          lambda x: x[1:],
        'cons':         lambda x, y: [x] + y,
        'eq?':          op.is_,
        'equal?':       op.eq,
        'length':       len,
        'list':         lambda *x: list(x),
        'list?':        lambda x: isinstance(x, p.List),
        'map':          map,
        'max':          max,
        'min':          min,
        'not':          op.not_,
        'null?':        lambda x: x == [],
        'number?':      lambda x: isinstance(x, p.Number),
        'procedure?':   callable,
        'round':        round,
        'symbol?':      lambda x: isinstance(x, p.Symbol),
    })

    return env


global_env = standard_env()


def eval(exp, env=global_env):
    """Evaluate an expression given an environment.

    Args:
        exp (scheme expression): Either a Symbol, Number,
            or List (representing an expression).
        env (dict): A mapping of scheme functions/vars/expressions
            to equivalent python expressions.

    Returns:
    """

    if isinstance(exp, p.Symbol):
        return env.find(exp)[exp]
    elif not isinstance(exp, p.List):
        return exp
    elif exp[0] == 'quote':
        (_, literal) = exp
        return literal
    elif exp[0] == 'if':
        (_, test, conseq, alt) = exp
        result = (conseq if eval(test, env) else alt)
        return eval(result, env)
    elif exp[0] == 'define':
        (_, var, assignment) = exp
        env[var] = eval(assignment, env)
    elif exp[0] == 'set!':
        (_, var, exp) = exp
        env.find(var)[var] = eval(exp, env)
    elif exp[0] == 'lambda':
        (_, parms, body) = exp
        return Procedure(parms, body, env)
    else:
        proc = eval(exp[0], env)
        args = [eval(arg, env) for arg in exp[1:]]
        return proc(*args)
