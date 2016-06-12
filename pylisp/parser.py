import re
import StringIO


from util import to_string


###############################################################################
# TYPES

# Symbols
class Symbol(str):
    pass


def Sym(s, symbol_table={}):
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)
    return symbol_table[s]


def let(*args):
    args = list(args)
    x = cons(_let, args)
    require(x, len(args) > 1)
    bindings, body = args[0], args[1:]
    require(x, all(isinstance(b, list) and len(b)==2 and isinstance(b[0], Symbol)
                   for b in bindings), "illegal binding list")


KEYWORDS = [
    "quote",
    "if",
    "set!",
    "define",
    "lambda",
    "begin",
    "define-macro",
    "quasiquote",
    "unquote",
    "unquote-splicing",
    "let",
    "append",
    "cons",
]


_quote, _if, _set, _define, _lambda, _begin, _definemacro, \
        _quasiquote, _unquote, _unquotesplicing, _let, _append, \
        _cons = map(Sym, KEYWORDS)

macro_table = {
    _let: let
}

eof_object = Symbol('#<eof-object>') # Note: uninterned; can't be read

# Other types TODO develop
List   = list
Number = (int, float)



################################################################################
# Parser

quotes = {"'":_quote, "`":_quasiquote, ",":_unquote, ",@":_unquotesplicing}

class InPort(object):
    "An input port. Retains a line of chars."
    tokenizer = r'''\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)'''
    def __init__(self, f):
        self.file = f;
        self.line = ''

    def next_token(self):
        "Return the next token, reading new text into line buffer if needed."
        while True:
            if self.line == '':
                self.line = self.file.readline()
            if self.line == '':
                return eof_object
            token, self.line = re.match(InPort.tokenizer, self.line).groups()
            if token != '' and not token.startswith(';'):
                return token


def parse(inport):
    if isinstance(inport, str):
        inport = InPort(StringIO.StringIO(inport))
    return expand(read(inport), toplevel=True)


def read(inport):
    """Read a Scheme expression from an input port.
    """
    def read_ahead(token):
        if '(' == token:
            L = []
            while True:
                token = inport.next_token()
                if token == ')':
                    return L
                else:
                    L.append(read_ahead(token))
        elif ')' == token:
            raise SyntaxError('unexpected )')
        elif token in quotes:
            return [quotes[token], read(inport)]
        elif token is eof_object:
            raise SyntaxError('unexpected EOF in list')
        else:
            return atom(token)
    # body of read
    token1 = inport.next_token()
    return eof_object if token1 is eof_object else read_ahead(token1)


def expand(x, toplevel=False):
    require(x, x!= [])
    if not isinstance(x, List):
        return x
    elif x[0] is _quote:
        require(x, len(x)==2)
        return x
    elif x[0] is _if:
        if len(x)==3:
            x = x + [None]
        require(x, len(x)==4)
        return map(expand, x)
    elif x[0] is _set:
        require(x, len(x)==3)
        require(x, isinstance(x[1], Symbol))
        return [_set, var, expand(x[2])]
    elif x[0] is _define or x[0] is _definemacro:
        require(x, len(x) >= 3)
        _def, var, body = x[0], x[1], x[2:]
        if isinstance(var, list) and var:
            f, args = v[0], v[1:]
            return expand
        else:
            require(x, len(x)==3)
            require(x, isinstance(var, Symbol), "Can only define symbols")
            exp = expand(x[2])
            if _def is _definemacro:
                require(x, toplevel, "define-macro only allowed at top level")
                proc = eval(exp)
                require(x, callable(proc), "macro must be a procedure")
                macro_table[v] = proc
                return None
            return [_define, var, exp]
    elif x[0] is _begin:
        if len(x)==1:
            return None
        else:
            return [expand(xi, toplevel) for xi in x]
    elif x[0] is _lambda:
        require(x, len(x) >= 3)
        var, body = x[1], x[2:]
        require(x, (isinstance(var, list) and all(isinstance(var, Symbol) for v in var))
                or isa(var, Symbol), "illegal lambda argument list")
        exp = body[0] if len(body) == 1 else [_begin] + body
        return [_lambda, var, expand(exp)]
    elif x[0] is _quasiquote:
        require(x, len(x)==2)
        return expand_quasiquote(x[1])
    elif isinstance(x[0], Symbol) and x[0] in macro_table:
        return expand(macro_table[x[0]](*x[1:]), toplevel)
    else:
        return map(expand, x)


def require(x, predicate, msg="wrong length"):
    """TODO
    """
    if not predicate:
        raise SyntaxError(r.to_string(x) + ": " + msg)


def expand_quasiquote(x):
    """Expand `x => 'x; `,x => x; `(,@x y) => (append x y) """
    if not is_pair(x):
        return [_quote, x]
    require(x, x[0] is not _unquotesplicing, "can't splice here")
    if x[0] is _unquote:
        require(x, len(x)==2)
        return x[1]
    elif is_pair(x[0]) and x[0][0] is _unquotesplicing:
        require(x[0], len(x[0])==2)
        return [_append, x[0][1], expand_quasiquote(x[1:])]
    else:
        return [_cons, expand_quasiquote(x[0]), expand_quasiquote(x[1:])]


def atom(token):
    """Numbers become numbers; #t and #f are booleans; "..." string; else
    return a Symbol.

    Argument:
        token (string): A string representing a Scheme type.

    Returns:
        The corresponding scheme type -- A boolean, int, float, complex, or
        string.
    """
    if token == '#t':
        return True
    elif token == '#f':
        return False
    elif token[0] == '"':
        return token[1:-1].decode('string_escape')
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            try:
                return complex(token.replace('i', 'j', 1))
            except ValueError:
                return Sym(token)
