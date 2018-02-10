from front_.lexer_ import Lexer
from front_.parser_ import Parser
from front_.generator import Generator, Generator_as
from front_.generator_dir.generator import Generator_as1
from util import *

def _main_():
    code = '{int a;a=1+2*3-4*2+4*(1+2)+1-2;' \
           'printf("%d\\n", a);}'

    lexer = Lexer(code)
    lexer.scan()
    tokens = lexer.tokens
    parser = Parser(tokens)
    # ir = Generator(ast)
    # gen = Generator_as(parser)
    gen = Generator_as1(parser)
    gen.gen_executable_ir()
    # gen.gen_test_ir()
    ir = gen.ir
    # ir = insert_(ir)
    # print(ir)
    f = open('/home/latin/code/python/latin_compiler/test.s', 'w')
    f.write(ir)


_main_()
