from front_.token import Token

symbols = [ '+', '-', '*', '/', '!', '=',
            '<', '<=', '>', '>=', '==', '!=',
            '&&', '||', '&', '|',
            '{', '}', '(', ')', '[', ']',
            ',', '.', '\'', '\"', ';', '%', '\\'
            ]
reserved_word = ['int', 'float', 'if', 'else', 'break', 'return',
'for', 'continue', 'while', 'do', 'printf', ]

class Lexer:
    def __init__(self, code):
        self.tokens = list()
        self.index = 0
        self.code = code + ' '
        self.len_ = len(code)
        self.setup()

    def setup(self):
        self.skip_space()

    def scan(self):
        while self.not_eof():
            t = self.scan_tok()
            self.tokens.append(t)

    def skip_space(self):
        while self.not_eof():
            c = self.cur_char()
            if c.isspace():
                self.next_index()
            else:
                return

    def not_eof(self):
        return self.index < self.len_

    def cur_char(self):
        return self.code[self.index]

    def next_char(self):
        c = self.cur_char()
        self.next_index()
        return c

    def next_index(self):
        self.index += 1

    def match(self, char):
        if self.index < len(self.code):
            c = self.cur_char()
            if c != char:
                print('not match!')
                print('last:  ', self.code[self.index-2], self.code[self.index-1])
                print('index: ', self.index, 'len:  ', len(self.code))
                print('match:  ', c)
                print('expect: ', char)
                raise Exception
            self.next_index()
        else:
            print('index out of range!')
            print('last:  ', self.code[self.index-1])
            print('expect: ', char)
            raise Exception

    def scan_tok(self):
        word = ''
        c = self.cur_char()
        if c.isalpha():
            t = self.scan_ident()
        elif c.isdigit():
            t = self.scan_num()
        elif c in symbols:
            t = self.scan_symbol()

        self.skip_space()
        return t

    def scan_symbol(self):
        type_ = 'symbol'
        word = self.symbol_word()
        return Token(word, type_)

    def symbol_word(self):
        c = self.next_char()
        if c == '<' or c == '>' or c == '!':
            next_c = self.cur_char()
            if next_c == '=':
                word = c + next_c
                self.next_char()
                return word
        elif c == '&' or c == '|' or c == '=':
            next_c = self.cur_char()
            if c == next_c:
                word = c + next_c
                self.next_char()
                return word
        elif c == '\\':
            next_c = self.cur_char()
            if next_c == 'n':
                word = '\\n'
                self.next_char()
                return word
            elif next_c == '\\':
                word = '\\\\'
                self.next_char()
                return word
        return c

    def scan_ident(self):
        word = self.ident_word()
        if word in reserved_word:
            type_ = 'reserved'
        else:
            type_ = 'identifier'
        return Token(word, type_)

    # def is_array(self):
    #     c = self.cur_char()
    #     return c == '['
    #
    # def array_index(self):
    #     self.match('[')
    #     c = self.cur_char()
    #     if c.isdigit():
    #         index = self.num_word()
    #     else:
    #         index = self.ident_word()
    #     self.match(']')
    #     return index

    def ident_word(self):
        word = ''
        c = self.cur_char()
        while c.isalnum() or c == '_':
            word += c
            self.next_char()
            c = self.cur_char()
        return word

    def scan_num(self):
        word = self.num_word()
        type_ = 'number'
        return Token(word, type_)

    def num_word(self):
        word = ''
        c = self.cur_char()
        while self.is_num(c):
            word += c
            self.next_char()
            c = self.cur_char()
        return word

    def is_num(self, char):
        return char.isdigit() or char == '.'
