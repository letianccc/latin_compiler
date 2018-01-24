from front_.token import Token


symbols = [ '+', '-', '*', '/', '!', '=',
            '<', '<=', '>', '>=', '==', '!=',
            '&&', '||', '&', '|',
            '{', '}', '(', ')',
            ',', '.', '\'', ';',
            ]
reserved_word = ['int', 'float', 'if', 'else', 'break', 'return',
'for', 'continue', 'while', 'do', ]

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
        while c.isalnum() or c == '_':
            word += c
            index += 1
            c = code[index]
        if word in reserved_word:
            type_ = 'reserved'
        else:
            type_ = 'identifier'
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
        word = c
        index += 1
        if c == '<' or c == '>' or c == '!':
            next_c = code[index]
            if next_c == '=':
                word += next_c
                index += 1
        elif c == '&' or c == '|' or c == '=':
            next_c = code[index]
            if c == next_c:
                word += next_c
                index += 1

    index = skip_space(code, index)
    t = Token(word, type_)
    return t, index
