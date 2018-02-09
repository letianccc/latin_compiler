from front_.lexer_ import Lexer
from front_.AST import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.symbols = list()
        self.printf_formats = list()
        self.symbol_count = 0
        self.ident_count = 0
        self.has_array = False
        self.has_printf = False
        self.AST = self.block_()

    def is_word(self, word):
        t = self.cur_token()
        if t.name == word:
            return True
        else:
            return False

    def is_type(self, type_):
        t = self.cur_token()
        if t.type_ == type_:
            return True
        else:
            return False

    def cur_token(self):
        return self.tokens[self.index]

    def next_token(self):
        t = self.tokens[self.index]
        self.increase_index()
        return t

    def last_token(self):
        return self.tokens[self.index-1]

    def increase_index(self):
        self.index += 1

    def return_token(self):
        self.index += 1

    def match(self, word):
        if self.index < len(self.tokens):
            name = self.cur_token().name
            if name != word:
                print('not match!')
                print('last:  ', self.tokens[self.index-4].name, self.tokens[self.index-3   ].name,
                      self.tokens[self.index-2].name, self.tokens[self.index-1].name)
                print('index: ', self.index, 'len:  ', len(self.tokens))
                print('match:  ', name)
                print('expect: ', word)
                raise Exception
            self.increase_index()
        else:
            print('index out of range!')
            print('last:  ', self.tokens[self.index-1].name)
            print('expect: ', word)
            raise Exception

    def block_(self):
        if self.is_word('{'):
            self.match('{')
            if self.is_type('number'):
                block = self.parse_array_data()
            else:
                block = self.stmts_()
            self.match('}')
        else:
            block = self.single_stmt()
        return block

    def stmts_(self):
        stmt = self.stmt_()
        if not self.is_word('}'):
            next_stmt = self.stmts_()
            stmt = Seq(stmt, next_stmt)
        return stmt

    def single_stmt(self):
        return self.stmt_()

    def stmt_(self):
        t = self.cur_token()
        name = t.name
        if self.is_word('if'):
            return self.if_stmt()
        elif self.is_word('int') or self.is_word('float'):
            return self.decl()
        elif self.is_word('while'):
            return self.while_stmt()
        elif self.is_word('printf'):
            return self.printf_stmt()
        elif self.is_word('{'):
            return self.block_()
        else:
            return self.assign()

    def parse_array_data(self):
        array = list()
        while True:
            t = self.next_token()
            num = t.name
            array.append(num)
            if self.is_word(','):
                self.match(',')
            else:
                # }
                break
        return Array_(array)

    def printf_stmt(self):
        self.has_printf = True
        self.match('printf')
        self.match('(')
        self.match('\"')
        format_ = self.parse_format()
        self.match('\"')
        if self.is_word(','):
            self.match(',')
            val = self.factor()
        self.match(')')
        self.match(';')
        return Printf(format_, val)

    def parse_format(self):
        format_ = self.format_word()
        if format_ not in self.printf_formats:
            self.printf_formats.append(format_)
        return format_

    def format_word(self):
        format_ = ''
        while not self.is_word('\"'):
            c = self.next_token().name
            format_ += c
        return format_

    def while_stmt(self):
        self.match('while')
        self.match('(')
        cond = self.bool_()
        self.match(')')
        suite = self.block_()
        return While(cond, suite)

    def if_stmt(self):
        self.match('if')
        self.match('(')
        cond = self.bool_()
        self.match(')')
        then_stmts = self.block_()
        if self.is_word('else'):
            self.match('else')
            else_stmts = self.block_()
        else:
            else_stmts = None
        return If(cond, then_stmts, else_stmts)

    def decl(self):
        type_ = self.next_token().name
        if self.is_array():
            self.has_array = True
            decl_ = self.decl_array(type_)
        else:
            decl_ = self.decl_single_variable(type_)
        self.match(';')
        return decl_

    def is_array(self):
        t = self.tokens[self.index + 1]
        if t.name == '[':
            return True
        else:
            return False

    def decl_array(self, type_):
        var = self.next_token()
        expr = self.parse_array_postfix() # expr是number类型
        array = Array(var, expr)
        array_size = int(expr.name)
        self.add_symbol(array, array_size)
        return Decl(type_, array)

    def parse_array_postfix(self):
        self.match('[')
        expr = self.expr_()
        self.match(']')
        return expr

    def is_num(self, array_node):
        n = array_node
        if n.__class__.__name__ == 'Token':
            if n.type_ == 'number':
                return True
        return False

    def decl_single_variable(self, type_):
        var = self.next_token()
        amount = 1
        self.add_symbol(var, amount)
        return Decl(type_, var)

    def add_symbol(self, symbol, amount):
        self.symbols.append(symbol)
        self.ident_count += amount
        self.symbol_count += amount

    def assign(self):
        variable = self.factor()
        self.match('=')
        value = self.bool_()
        self.match(';')
        return Assign(variable, value)

    def bool_(self):
        expr = self.join()
        while self.is_word('||'):
            self.match('||')
            expr = Or(expr, self.join())
        return expr

    def join(self):
        expr = self.equal()
        while self.is_word('&&'):
            self.match('&&')
            expr = And(expr, self.equal())
        return expr

    def equal(self):
        expr = self.rel()

        while self.is_word('==') or self.is_word('!='):
            operator = self.next_token().name
            expr = Equal(expr, self.rel(), operator)
        return expr

    def rel(self):
        expr = self.expr_()
        while self.is_word('<') or self.is_word('<=') or self.is_word('>') or self.is_word('>='):
            operator = self.next_token().name
            expr = Rel(expr, self.expr_(), operator)
        return expr

    def expr_(self):
        expr = self.term()

        while self.is_word('+') or self.is_word('-'):
            self.symbol_count += 1
            operator = self.next_token().name
            expr = Arith(expr, self.term(), operator)
        return expr

    def term(self):
        expr = self.unary()

        while self.is_word('*') or self.is_word('/'):
            self.symbol_count += 1
            operator = self.next_token().name
            expr = Arith(expr, self.unary(), operator)
        return expr

    def unary(self):
        if self.is_word('!') or self.is_word('-'):
            operator = self.next_token().name
            expr = Unary(operator, self.factor())
        else:
            expr = self.factor()
        return expr

    def factor(self):
        if self.is_word('('):
            self.match('(')
            expr = self.bool_()
            self.match(')')
            return expr
        elif self.is_word('{'):
            return self.block_()
        elif self.is_array():
            name = self.next_token()
            index = self.parse_array_element()
            return Array(name, index)
        else:
            # 标识符
            return self.next_token()

    def parse_array_element(self):
        array_index = self.parse_array_postfix()
        if not self.is_num(array_index):
            self.symbol_count += 1
        return array_index
