from front_.lexer_ import skip_space, scan_tok, lexer
from front_.parser_ import Parser
from front_.generator import Generator, Generator_as
from util import *

i = 0
all_ = True

def test_gen():
    code = '{{{int a;a=2;}}}'
    test_ir = 'L1: t0 = 2\n' \
              'L2: End\n'
    test(code, test_ir)

    code = '{int a;a=-2;int b;b=4;}'
    test_ir = 'L1: t0 = -2\n' \
              'L2: t1 = 4\n' \
              'L3: End\n'
    test(code, test_ir)

    code = '{int a; a=-2; int b; b=4; a = a + a * (2 + 3) - b - a / 4 + b + 5 / (a + 3) + 5;}'
    test_ir = 'L1: t0 = -2\n'          \
              'L2: t1 = 4\n'          \
              'L3: t2 = 2 + 3\n'      \
              'L4: t3 = t0 * t2\n'    \
              'L5: t4 = t0 + t3\n'    \
              'L6: t5 = t4 - t1\n'    \
              'L7: t6 = t0 / 4\n'     \
              'L8: t7 = t5 - t6\n'    \
              'L9: t8 = t7 + t1\n'    \
              'L10: t9 = t0 + 3\n'    \
              'L11: t10 = 5 / t9\n'   \
              'L12: t11 = t8 + t10\n' \
              'L13: t12 = t11 + 5\n'  \
              'L14: t0 = t12\n'       \
              'L15: End\n'
    test(code, test_ir)

    code = '{int a; a=2; int c; c = a < 1;}'
    test_ir = 'L1: t0 = 2\n'        \
              'L2: t2 = t0 < 1\n'   \
              'L3: t1 = t2\n'       \
              'L4: End\n'
    test(code, test_ir)

    code = '{int a; a=2; int c; c = !(a < 1 && a>2);}'
    test_ir = 'L1: t0 = 2\n'        \
              'L2: t2 = t0 < 1\n'   \
              'L3: t3 = t0 > 2\n'   \
              'L4: t4 = t2 && t3\n'   \
              'L5: t1 = !t4\n'       \
              'L6: End\n'
    test(code, test_ir)

    code = '{int a; a=2; int b; b=4; int c; ' \
           'c = a < 1 || b > 2 && a <= 3 || !(a >= 2 || b < 3) && b < 2;}'
    test_ir = 'L1: t0 = 2\n'             \
              'L2: t1 = 4\n'             \
              'L3: t3 = t0 < 1\n'        \
              'L4: t4 = t1 > 2\n'        \
              'L5: t5 = t0 <= 3\n'        \
              'L6: t6 = t4 && t5\n'      \
              'L7: t7 = t3 || t6\n'      \
              'L8: t8 = t0 >= 2\n'        \
              'L9: t9 = t1 < 3\n'        \
              'L10: t10 = t8 || t9\n'    \
              'L11: t11 = t1 < 2\n'      \
              'L12: t12 = !t10 && t11\n'  \
              'L13: t13 = t7 || t12\n'   \
              'L14: t2 = t13\n'          \
              'L15: End\n'
    test(code, test_ir)

    code = '{int a; a=2; int b; b=4; int c; ' \
           'if(a < 1 || b > 2 && a <= 3 || (a >= 2 || b != 3) && b == 2)c=2;else c=3;}'
    test_ir = 'L1: t0 = 2\n'             \
              'L2: t1 = 4\n'             \
              'L3: t3 = t0 < 1\n'        \
              'L4: t4 = t1 > 2\n'        \
              'L5: t5 = t0 <= 3\n'        \
              'L6: t6 = t4 && t5\n'      \
              'L7: t7 = t3 || t6\n'      \
              'L8: t8 = t0 >= 2\n'        \
              'L9: t9 = t1 != 3\n'        \
              'L10: t10 = t8 || t9\n'    \
              'L11: t11 = t1 == 2\n'      \
              'L12: t12 = t10 && t11\n'  \
              'L13: t13 = t7 || t12\n'   \
              'L14: if t13 is false goto L17\n' \
              'L15: t2 = 2\n'                 \
              'L16: goto L18\n'                \
              'L17: t2 = 3\n'                 \
              'L18: End\n'
    test(code, test_ir)

    code = '{int a;a=1;if(a==1)a=2;else a=3;}'
    test_ir =  'L1: t0 = 1\n'                 \
               'L2: t1 = t0 == 1\n'           \
               'L3: if t1 is false goto L6\n' \
               'L4: t0 = 2\n'                 \
               'L5: goto L7\n'                \
               'L6: t0 = 3\n'                 \
               'L7: End\n'
    test(code, test_ir)

    code = '{int a;a=1;if(a==1){a=2;}else{a=3;}}'
    test_ir =  'L1: t0 = 1\n'                 \
               'L2: t1 = t0 == 1\n'           \
               'L3: if t1 is false goto L6\n' \
               'L4: t0 = 2\n'                 \
               'L5: goto L7\n'                \
               'L6: t0 = 3\n'                 \
               'L7: End\n'
    test(code, test_ir)

    code = '{int a;a=1;if(a==1)a=2;}'
    test_ir =  'L1: t0 = 1\n'                 \
               'L2: t1 = t0 == 1\n'           \
               'L3: if t1 is false goto L6\n' \
               'L4: t0 = 2\n'                 \
               'L5: goto L6\n'                \
               'L6: End\n'
    test(code, test_ir)

    code = '{int a;a=1;if(a==1){a=2;}}'
    test_ir =  'L1: t0 = 1\n'                 \
               'L2: t1 = t0 == 1\n'           \
               'L3: if t1 is false goto L6\n' \
               'L4: t0 = 2\n'                 \
               'L5: goto L6\n'                \
               'L6: End\n'
    test(code, test_ir)

    code = '{int a;a=4;while(a>0)a=a-1;}'
    test_ir =  'L1: t0 = 4\n'                 \
               'L2: t1 = t0 > 0\n'           \
               'L3: if t1 is false goto L7\n' \
               'L4: t2 = t0 - 1\n'                 \
               'L5: t0 = t2\n'                 \
               'L6: goto L2\n'                \
               'L7: End\n'
    test(code, test_ir)

    code = '{int a;a=4;while(a>0){a=a-1;}}'
    test_ir =  'L1: t0 = 4\n'                 \
               'L2: t1 = t0 > 0\n'           \
               'L3: if t1 is false goto L7\n' \
               'L4: t2 = t0 - 1\n'                 \
               'L5: t0 = t2\n'                 \
               'L6: goto L2\n'                \
               'L7: End\n'
    test(code, test_ir)

def test__as():
    code = '{int a;a=2;}'
    test_ir = 'movl $2, %eax\n' \
              'movl %eax, -4(%rbp)\n'
    test1(code, test_ir)

    code = '{int a;a=2;int b; b=4;}'
    test_ir = 'movl $2, %eax\n' \
              'movl %eax, -4(%rbp)\n' \
              'movl $4, %eax\n' \
              'movl %eax, -8(%rbp)\n'
    test1(code, test_ir)

    code = '{int a;a=1+2;}'
    test_ir = 'movl $1, %eax\n'\
              'movl $2, %edx\n'\
              'addl %edx, %eax\n'\
              'movl %eax, -8(%rbp)\n'\
              'movl -8(%rbp), %eax\n'\
              'movl %eax, -4(%rbp)\n'
    test1(code, test_ir)

    code = '{int a;a=1*2;}'
    test_ir = 'movl $1, %eax\n'\
              'movl $2, %edx\n'\
              'imull %edx, %eax\n'\
              'movl %eax, -8(%rbp)\n'\
              'movl -8(%rbp), %eax\n'\
              'movl %eax, -4(%rbp)\n'
    test1(code, test_ir)

    code = '{int a;a=1+2*3;}'
    test_ir = 'movl $2, %eax\n'\
              'movl $3, %edx\n'\
              'imull %edx, %eax\n'\
              'movl %eax, -8(%rbp)\n'\
              'movl $1, %eax\n'\
              'movl -8(%rbp), %edx\n'\
              'addl %edx, %eax\n'\
              'movl %eax, -12(%rbp)\n'\
              'movl -12(%rbp), %eax\n'\
              'movl %eax, -4(%rbp)\n'
    test1(code, test_ir)

    code = '{int a;a=1+2*3;}'
    test_ir = 'movl $2, %eax\n'\
              'movl $3, %edx\n'\
              'imull %edx, %eax\n'\
              'movl %eax, -8(%rbp)\n'\
              'movl $1, %eax\n'\
              'movl -8(%rbp), %edx\n'\
              'addl %edx, %eax\n'\
              'movl %eax, -12(%rbp)\n'\
              'movl -12(%rbp), %eax\n'\
              'movl %eax, -4(%rbp)\n'
    test1(code, test_ir)

    # code = '{int a;a=1+2*3-4*2+4*(1+2)+1-2;}'

    code = '{int a;a=1;if(a==1)a=2;}'
    test_ir = 'movl $1, %eax\n'\
                'movl %eax, -4(%rbp)\n'\
                'cmpl $1, -4(%rbp)\n'\
                'jne .L2\n'\
                '.L1:\n'\
                'movl $2, %eax\n'\
                'movl %eax, -4(%rbp)\n'\
                '.L2:\n'
    test1(code, test_ir)

    code = '{int a;a=1;if(a==1)a=2;else a=3;}'
    test_ir = 'movl $1, %eax\n'\
              'movl %eax, -4(%rbp)\n'\
              'cmpl $1, -4(%rbp)\n'\
              'jne .L2\n'\
              '.L1:\n'\
              'movl $2, %eax\n'\
              'movl %eax, -4(%rbp)\n'\
              'jmp .L3\n'\
              '.L2:\n'\
              'movl $3, %eax\n'\
              'movl %eax, -4(%rbp)\n'\
              '.L3:\n'
    test1(code, test_ir)

    code = '{int a; a=2; int b; b=4; int c; ' \
           'if(a < 1 || b > 2 && a <= 3 || (a >= 2 || b != 3) && b == 2)c=2;else c=3;}'
    test_ir =   'movl $2, %eax\n'\
                'movl %eax, -4(%rbp)\n'\
                'movl $4, %eax\n'\
                'movl %eax, -8(%rbp)\n'\
                'cmpl $1, -4(%rbp)\n'\
                'jl .L1\n'\
                'cmpl $2, -8(%rbp)\n'\
                'jle .L4\n'\
                'cmpl $3, -4(%rbp)\n'\
                'jle .L1\n'\
                '.L4:\n'\
                'cmpl $2, -4(%rbp)\n'\
                'jge .L5\n'\
                'cmpl $3, -8(%rbp)\n'\
                'je .L2\n'\
                '.L5:\n'\
                'cmpl $2, -8(%rbp)\n'\
                'jne .L2\n'\
                '.L1:\n'\
                'movl $2, %eax\n'\
                'movl %eax, -12(%rbp)\n'\
                'jmp .L3\n'\
                '.L2:\n'\
                'movl $3, %eax\n'\
                'movl %eax, -12(%rbp)\n'\
                '.L3:\n'
    test1(code, test_ir)


def test1(code, test_ir):
    if all_:
        tokens = lexer(code)
        # print_token_names(tokens)
        parser = Parser(tokens)
        ast = parser.AST
        gen = Generator_as(ast)
        try:
            assert(gen.ir == test_ir)
        except:
            print(code)
            print(gen.ir)
    else:
        global i
        i += 1
        if i == 4:
            tokens = lexer(code)
            print_token_names(tokens)
            parser = Parser(tokens)
            ast = parser.AST
            gen = Generator_as(ast)
            assert(gen.ir == test_ir)



def test(code, test_ir):
    if all_:
        tokens = lexer(code)
        # print_token_names(tokens)
        parser = Parser(tokens)
        ast = parser.AST
        gen = Generator(ast)
        assert(gen.ir == test_ir)
    else:
        global i
        i += 1
        if i == 4:
            tokens = lexer(code)
            print_token_names(tokens)
            parser = Parser(tokens)
            ast = parser.AST
            gen = Generator(ast)
            assert(gen.ir == test_ir)




test_gen()
test__as()
