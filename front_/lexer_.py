from front_.token import Token
from util import print_list


symbols = ['+', '-', '*', '/', '{', '}', ',', '.', '\'', ';']
index = 0

def lexer(code):
    tokens = list()
    code += ' '
    len_ = len(code)
    index = 0
    index = skip_space(code, index)
    while index < len_:
        t, index = scan_tok(code, index)
        tokens.append(t)
    return tokens


def skip_space(code, index):
    while index < len(code) and code[index].isspace():
        index += 1
    return index


def scan_tok(code, index):


    word = ""
    c = code[index]
    if c.isalpha():
        # 标识符
        type_ = 'identifier'
        while c.isalnum() or c == '_':
            word += c
            index += 1
            c = code[index]
    elif c.isdigit():
        # 数字
        type_ = 'number'
        while c.isdigit() or c == '.':
            word += c
            index += 1
            c = code[index]
    elif c in symbols:
        # 分隔符
        type_ = 'symbol'
        word += c
        index += 1

    index = skip_space(code, index)
    t = Token(word, type_)


    return t, index

def test_scan_tok():
    code = 'abc123_a'
    code += ' '
    index = 0
    index = skip_space(code, index)
    t, index = scan_tok(code, index)
    assert (t.name == 'abc123_a')
    assert (t.type_ == 'identifier')

    code = '  abc123_a '
    code += ' '
    index = 0
    index = skip_space(code, index)
    t, index = scan_tok(code, index)
    assert (t.name == 'abc123_a')
    assert (t.type_ == 'identifier')

    code = '  abc123_a a'
    code += ' '
    index = 0
    index = skip_space(code, index)
    t, index = scan_tok(code, index)
    assert(t.name == 'abc123_a')
    assert(t.type_ == 'identifier')

    code = '  abc123_aa '
    code += ' '
    index = 0
    index = skip_space(code, index)
    t, index = scan_tok(code, index)
    assert (t.name == 'abc123_aa')
    assert (t.type_ == 'identifier')

    code = '   abc123_aa 11 '
    code += ' '
    index = 0
    index = skip_space(code, index)
    t, index = scan_tok(code, index)
    assert (t.name == 'abc123_aa')
    assert (t.type_ == 'identifier')

    code = '  11 '
    code += ' '
    index = 0
    index = skip_space(code, index)
    t, index = scan_tok(code, index)
    assert (t.name == '11')
    assert (t.type_ == 'number')


def test_lexer():
    code = '  abc123_a a '
    tokens = lexer(code)
    assert(tokens[0].name == 'abc123_a')
    assert (tokens[0].type_ == 'identifier')
    assert (tokens[1].name == 'a')
    assert (tokens[1].type_ == 'identifier')

    code = 'abc123_a a 213'
    tokens = lexer(code)
    assert (tokens[0].name == 'abc123_a')
    assert (tokens[0].type_ == 'identifier')
    assert (tokens[1].name == 'a')
    assert (tokens[1].type_ == 'identifier')
    assert (tokens[2].name == '213')
    assert (tokens[2].type_ == 'number')

    code = '  abc123_a a 123 '
    tokens = lexer(code)
    assert (tokens[0].name == 'abc123_a')
    assert (tokens[0].type_ == 'identifier')
    assert (tokens[1].name == 'a')
    assert (tokens[1].type_ == 'identifier')
    assert (tokens[2].name == '123')
    assert (tokens[2].type_ == 'number')

    code = '{int a;}'
    tokens = lexer(code)
    assert (tokens[0].name == '{')
    assert (tokens[0].type_ == 'symbol')
    assert (tokens[1].name == 'int')
    assert (tokens[1].type_ == 'identifier')
    assert (tokens[2].name == 'a')
    assert (tokens[2].type_ == 'identifier')
    assert (tokens[3].name == ';')
    assert (tokens[3].type_ == 'symbol')
    assert (tokens[4].name == '}')
    assert (tokens[4].type_ == 'symbol')

test_scan_tok()
test_lexer()
