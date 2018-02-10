import subprocess
from front_.lexer_ import Lexer
from front_.parser_ import Parser
from front_.generator import Generator, Generator_as
from front_.generator_dir.generator import Generator_as1
import os


def test_case():
    case = dict()

    # assign, arith
    code = '{int a;a=2;}'
    result = ''
    case[code] = result

    code = '{int a;a=2;int b; b=4;}'
    result = ''
    case[code] = result

    code = '{int a;a=1+2;}'
    result = ''
    case[code] = result

    code = '{int a;a=1*2;}'
    result = ''
    case[code] = result

    code = '{int a;a=1+2*3;}'
    result = ''
    case[code] = result

    code = '{int a;a=1+2*3;}'
    result = ''
    case[code] = result

    code = '{int a;a=1+2*3-4*2+4*(1+2)+1-2;' \
           'printf("%d\\n", a);}'
    result = '10\n'
    case[code] = result

    # array
    code = '{int a[5]; a[5] = {1,2};' \
           'printf("%d\\n",a[0]);' \
           'printf("%d\\n",a[1]);' \
           'printf("%d\\n",a[2]);' \
           'printf("%d\\n",a[3]);' \
           'printf("%d\\n",a[4]);}'
    result = '1\n2\n0\n0\n0\n'
    case[code] = result

    code = '{int b;b=2;int a[5];a[b]=4;printf("%d\\n",a[2]);}'
    result = '4\n'
    case[code] = result

    code = '{int b;b=2;int a[5];a[b+1]=4;printf("%d\\n",a[3]);}'
    result = '4\n'
    case[code] = result

    code = '{int a[3];a[3]={11, 22, 33};'\
        'int i;i=0;'\
        'a[i+2]=a[i];' \
        'printf("%d\\n", a[i+2]);'\
        'a[i+2]=a[i+1];' \
        'printf("%d\\n", a[i+2]);'\
        '}'
    result = '11\n22\n'
    case[code] = result

    # if
    code = '{int a;a=1;if(a==1)a=2;}'
    result = ''
    case[code] = result

    code = '{int a;a=1;if(a==1)a=2;else a=3;}'
    result = ''
    case[code] = result

    code = '{int a; a=2; int b; b=4; int c; ' \
           'if(a < 1 || b > 2 && a <= 3 || (a >= 2 || b != 3) && b == 2)c=2;else c=3;}'
    result = ''
    case[code] = result

    code = '{int x[5]; x[0]=2; x[1]=4;' \
           'if(x[0] < 1 || x[1] > 2 && x[0] <= 3 || (x[0] >= 2 || x[1] != 3) && x[1] == 2)x[2]=2;else x[2]=3;' \
           'printf("%d\\n", x[2]);}'
    result = '2\n'
    case[code] = result

    code = '{int a[2];a[2]={11, 22};'\
    'int i;i=0;'\
    'if(a[i]<a[i+1]){' \
        'a[i]=1;' \
    '} else{' \
        'a[i]=0;' \
    '}'\
    'printf("%d\\n", a[i]);'\
    '}'
    result = '1\n'
    case[code] = result

    # printf
    code = '{int a;a=2;printf("%d\\n",a);}'
    result = '2\n'
    case[code] = result

    # while
    code = '{int a;a=1;int b;b=1;' \
           'while(a<5){b=b+2;a=a+1;}' \
           'printf("%d\\n",b);}'
    result = '9\n'
    case[code] = result

    code = '{int a;a=0;int b;b=0;int c;c=0;' \
           'while(a<5){' \
           'while(b<5){' \
           'c=c+1;' \
           'b=b+1;' \
           '}' \
           'a=a+1;' \
           'b=0;' \
           '}' \
           'printf("%d\\n",c);}'
    result = '25\n'
    case[code] = result

    code = '{int a[4];a[4]={11, 22, 33};'\
    'int n;n=2;int i;i=0;'\
    'while(i<n){' \
        'a[i] = a[i+1];'\
        'i=i+1;'\
    '}'\
    'i=0;n=4;'\
    'while(i<n){' \
        'printf("%d\\n", a[i]);'\
        'i=i+1;'\
    '}}'
    result = '22\n33\n33\n0\n'
    case[code] = result

    # other
    code = '{int a[3];a[3]={11, 22, 33};'\
    'int i;i=0;'\
    'if(a[i]<a[i+1]){' \
        'a[i+2]=a[i];' \
    '} else{' \
        'a[i+2]=a[i+1];' \
    '}'\
    'printf("%d\\n", a[i]);'\
    'printf("%d\\n", a[i+1]);'\
    'printf("%d\\n", a[i+2]);'\
    '}'
    result = '11\n22\n11\n'
    case[code] = result

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
    result = '12\n15\n24\n45\n51\n78\n84\n95\n'
    case[code] = result

    return case

def test_exec():
    init_path()
    case = test_case()
    exec_results = exec_case(case)
    check_results(case, exec_results)

def init_path():
    path = '/home/latin/code/python/latin_compiler'
    os.chdir(path)

def exec_case(test_case):
    results = dict()
    for code, test_result in test_case.items():
        write_as_to_file(code)
        result = exec_as_file()
        results[code] = result
    return results

def write_as_to_file(code):
    lexer = Lexer(code)
    lexer.scan()
    tokens = lexer.tokens
    parser = Parser(tokens)
    # gen = Generator_as(parser)
    gen = Generator_as1(parser)
    gen.gen_executable_ir()
    # gen.gen_test_ir()
    ir = gen.ir
    # ir = insert_(ir)
    # print(ir)
    f = open('/home/latin/code/python/latin_compiler/test.s', 'w')
    f.write(ir)

def exec_as_file():
    subprocess.run("gcc -o test test.s", shell = True, check=True)
    x = subprocess.run("./test", stdout=subprocess.PIPE,shell = True)
    result = x.stdout.decode()
    return result

def check_results(test_case, exec_results):
    for code in test_case.keys():
        r = exec_results[code]
        test_result = test_case[code]
        try:
            assert(r == test_result)
        except:
            print(code)
            print('exec_result: ', r)
            print('test_result: ', test_result)
            print()

test_exec()
