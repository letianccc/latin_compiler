from front_.lexer_ import lexer
from front_.parser_ import Parser
from front_.generator import Generator, Generator_as
from util import *

def _main_():
    code = '{int a; a=2; int b; b=4; int c; ' \
           'if(a < 1 || b > 2 && a <= 3 || (a >= 2 || b != 3) && b == 2)c=2;else c=3;}'

    # code = '{int a; a=2; int b; b=4; int c; ' \
    #        'if(a < 3 || b > 2 && a <= 3 || (a >= 2 || b != 3) && b == 2)a=2;else a=3;}'

    # code = '{int a; a=2; int b; b=4; int c; ' \
    #        'if((a < 1 || b > 2) && a <= 3 )c=2;else c=3;}'
    # code = '{int a; a=2; int b; b=4; int c; ' \
    #        'if(a < 1 || b > 2 && a <= 3 )c=2;else c=3;}'
    # code = '{int a; a=2; int b; b=4; int c; ' \
    #        'if(a < 1 || b > 2 && a <= 3 || b == 2)c=2;else c=3;}'


    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.AST
    # ir = Generator(ast)
    gen = Generator_as(ast)
    ir = gen.ir
    ir = insert_(ir)
    # print(ir)
    f = open('/home/latin/code/python/latin_compiler/test.s', 'w')
    f.write(ir)


_main_()
