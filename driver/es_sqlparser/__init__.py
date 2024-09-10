from .lexer import Lexer
from .parser import Parser


debug = False


def do_test():
    global debug
    debug = True


def parse_handle(sql):
    L = Lexer(debug=debug)
    P = Parser(lexer=L, debug=debug)
    return P.parse(sql)
