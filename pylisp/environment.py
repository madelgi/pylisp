import math
import operator as op
import pylisp.parser as p
import pylisp.repl as r


################################################################################
## Environment class and global environment definition

class Env(dict):
    def __init__(self, parameters=(), args=(), outer=None):
        """An environment is a dict of {'var': val} pairs, with an
        (optional) outer Env.

        Args:
            parameters (list): A list of variable strings, e.g.,
                'x', 'y', 'z', 'double'
            args (list): A list of associated values for the parameters,
                e.g., 1, 2, 3, 'lambda x: x*2'
            outer (Env): An optional outer environment -- represents
                environment variables up a level in scope. At the top
                level, this will be None
        """
        self.outer = outer
        if isinstance(parameters, p.Symbol):
            self.update({parameters:list(args)})
        else:
            if len(args) != len(parameters):
                raise TypeError('Expected {0}, given {1}'.format(
                    r.to_string(parameters),
                    r.to_string(args)
                ))
            self.update(zip(parameters, args))

    def find(self, var):
        """Find the innermost Env where var appears. Cascade through
        outer envs until you come across an associated value.

        Args:
            A variable to search for.

        Returns:
            The environment containing the parameter.
        """
        if var in self:
            return self
        elif self.outer is None:
            raise LookupError(var)
        else:
            return self.outer.find(var)


def standard_env():
    """The standard set of environment variable-value pairs.

    Returns:
        An environment containing a bunch of standard operations.
    """
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
        'call/cc':      callcc,
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
        'read-char':    readchar,
        'symbol?':      lambda x: isinstance(x, p.Symbol),
    })
    return env


################################################################################
## Special operation definitions

def readchar(inport):
    """Read the next character from an input port.

    Args:
        inport (InPort): The inport to read from

    Returns:
        The next character in the input string

    Effects:
        Increments the inport.line attribute by one
    """
    if inport.line != '':
        ch, inport.line = inport.line[0], inport.line[1:]
        return ch
    else:
        return inport.file.read(1) or eof_object


def callcc(proc):
    """Call procedure with current continuation; escape only.

    Args:
        proc (Procedure): TODO
    """
    ball = RuntimeWarning("Sorry, can't continue this continuation any longer.")
    def throw(retval):
        ball.retval = retval
        raise ball
    try:
        return proc(throw)
    except RuntimeWarning as w:
        if w is ball:
            return ball.retval
        else:
            raise w


# Export a global environment
global_env = standard_env()
