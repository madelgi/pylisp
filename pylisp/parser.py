# Basic Scheme types.
Symbol = str
List   = list
Number = (int, float)

def parse(program):
    """Takes a string as input and outputs a syntax tree (in the
    form of a nested list).

    Args:
        program (str): A lisp program in the form of a string.

    Returns:
        A nested list representing the program logic.

    Examples:
        >>> parse("(if (= 3 3) (+ 1 2.72) 'nope')")
        ['if', ['=', 3, 3], ['+', 1, 2.72], "'nope'"]

    """
    return read_from_tokens(tokenize(program))

def tokenize(chars):
    """A very rudimentary tokenization function -- simply inserts spaces
    before and after parens, then splits the string.

    Args:
        chars (str)

    Returns:
        A list of characters.

    Examples:
        >>> tokenize("(if (= 3 3) (+ 1 2.72) 'nope')")
        ['(', 'if', '(', '=', '3', '3', ')', '(', '+', '1', '2.72', ')', "'nope'", ')']
    """
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def read_from_tokens(tokens):
    """Take a list of tokens and convert it into an abstract syntax tree.

    Args:
        tokens ([chars]): A list of tokens.

    Returns:
        An abstract syntax tree -- in this case, a nested list representing the
        program logic.

    Examples:
        >>> read_from_tokens(['(', 'if', '(', '=', '3', '3', ')', '(', '+', '1', '2.72', ')', "'nope'", ')'])
        ['if', ['=', 3, 3], ['+', 1, 2.72], "'nope'"]
    """
    if len(tokens) == 0:
        raise SyntaxError('Unexpected EOF while reading.')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif ')' == token:
        raise SyntaxError('Unexpected closing parenthesis, \')\'')
    else:
        return atom(token)

def atom(token):
    """Convert token to atom.

    Arg:
        token (char): A single token representing an atomic value in lisp.

    Return:
        An int, float, or string

    Examples:
        >>> atom('3')
        3
        >>> atom('3.14159')
        3.14159
        >>> atom('hello')
        hello
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)
