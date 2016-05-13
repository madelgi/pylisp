import parser as p
import evaluator as e


def repl(prompt='pylisp> '):
    """A prompt-read-eval-print loop.

    Args:
        prompt (str): The symbol that initializes the pylisp prompt. Defaults
            to `pylisp>`
    """
    while True:
        val = e.eval(p.parse(raw_input(prompt)))
        if val is not None:
            print(schemestr(val))


def schemestr(exp):
    """Convert a Python object back into a Scheme-readable string.

    Args:
        exp (list or ): TODO
    """
    if isinstance(exp, list):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)
