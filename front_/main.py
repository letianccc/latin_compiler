from front_.lexer_ import Lexer
from front_.parser_ import Parser
from front_.generator import Generator, Generator_as
from util import *

def _main_():

    # code = '{int b;b=2;int a[5];a[b+1]=4;printf("%d\\n",a[3]);}'

    code = '{int a[8];a[8]={45, 95, 15, 78, 84, 51, 24, 12};'\
    'int n;n=8;int i;int j;j=0;int temp;'\
    'while(j<n-1){' \
        'i=0;'\
        'while(i<n-1-j){' \
            'if(a[i]>a[i+1]){' \
                'temp=a[i];' \
                'a[i]=a[i+1];'\
                'a[i+1]=temp;'\
            '}'\
            'i=i+1;'\
        '}'\
        'j=j+1;'\
    '}'\
    'i=0;'\
    'while(i<n){' \
    'printf("%d\\n",a[i]);i=i+1;' \
    '}}'

    # code = '{int a[4];a[4]={11, 22, 33};'\
    # 'int n;n=4;int i;i=0;'\
    # 'while(i<n){' \
    #     'a[i] = i;'\
    #     'i=i+1;'\
    # '}'\
    # 'i=0;'\
    # 'while(i<n){' \
    #     'printf("%d\\n", a[i]);'\
    #     'i=i+1;'\
    # '}}'\
    # 0 1 2 3


    # code = '{int a[4];a[4]={11, 22, 33};'\
    # 'int n;n=2;int i;i=0;'\
    # 'while(i<n){' \
    #     'a[i] = a[i+1];'\
    #     'i=i+1;'\
    # '}'\
    # 'i=0;n=4;'\
    # 'while(i<n){' \
    #     'printf("%d\\n", a[i]);'\
    #     'i=i+1;'\
    # '}}'\
    # 22 33 33 0

    # code = '{int a[2];a[2]={11, 22};'\
    # 'int i;i=0;'\
    # 'a[i] = a[i+1];'\
    # 'printf("%d\\n", a[i]);'\
    # 'printf("%d\\n", a[i+1]);'\
    # '}'
    # 22 22



    # code = '{int a[2];a[2]={11, 22};'\
    # 'int i;i=0;'\
    # 'if(a[i]<a[i+1]){' \
    #     'a[i]=1;' \
    # '} else{' \
    #     'a[i]=0;' \
    # '}'\
    # 'printf("%d\\n", a[i]);'\
    # '}'
    # 1

    # code = '{int a[3];a[3]={11, 22, 33};'\
    # 'int i;i=0;'\
    # 'if(a[i]<a[i+1]){' \
    #     'a[i+2]=a[i];' \
    # '} else{' \
    #     'a[i+2]=a[i+1];' \
    # '}'\
    # 'printf("%d\\n", a[i]);'\
    # 'printf("%d\\n", a[i+1]);'\
    # 'printf("%d\\n", a[i+2]);'\
    # '}'
    # 11 22 11

    # code = '{int a[3];a[3]={11, 22, 33};'\
    # 'int i;i=0;'\
    # 'a[i+2]=a[i];' \
    # 'printf("%d\\n", a[i+2]);'\
    # 'a[i+2]=a[i+1];' \
    # 'printf("%d\\n", a[i+2]);'\
    # '}'
    # 11 22


    # 'printf("\n");}'
    # code = '{int a;a=0;int b;b=0;int c;c=0;' \
    #        'while(a<5){' \
    #        'while(b<5){' \
    #        'c=c+1;' \
    #        'b=b+1;' \
    #        '}' \
    #        'a=a+1;' \
    #        'b=0;' \
    #        '}' \
    #        'printf("%d\\n",c);}'
    # 25

    # code = '{int n;n=4;int i;i=0;int j;j=0;'\
    # 'while(i<n-1){' \
    #     'j=0;'\
    #     'while(j<n-1-i){' \
    #         'printf("%d\\n", i);\n'\
    #         'j=j+1;'\
    #     '}'\
    #     'i=i+1;'\
    # '}'\
    # '}'




    lexer = Lexer(code)
    lexer.scan()
    tokens = lexer.tokens
    parser = Parser(tokens)
    # ir = Generator(ast)
    gen = Generator_as(parser)
    gen.gen_executable_ir()
    # gen.gen_test_ir()
    ir = gen.ir
    # ir = insert_(ir)
    # print(ir)
    f = open('/home/latin/code/python/latin_compiler/test.s', 'w')
    f.write(ir)


_main_()
