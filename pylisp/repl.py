import parser as p
import evaluator as e
import sys


from util import to_string


def load(filename):
    """Eval every expression from a file.
    """
    repl(None, p.InPort(open(filename)), None)

def repl(prompt='lispy> ', inport=p.InPort(sys.stdin), out=sys.stdout):
    """A prompt-read-eval-print loop.
    """
    sys.stderr.write("Lispy version 2.0\n")
    while True:
        try:
            if prompt:
                sys.stderr.write(prompt)
            x = p.parse(inport)
            if x is p.eof_object:
                return
            val = e.eval(x)
            if val is not None and out:
                print >> out, to_string(val)
        except Exception, ex:
            print '{0}: {1}'.format(type(ex).__name__, ex)
            break
