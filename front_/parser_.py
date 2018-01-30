from front_.lexer_ import lexer
from front_.AST import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.AST = self.block_()

    def is_word(self, word):
        t = self.cur_token()
        if t.name == word:
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
                print('last:  ', self.tokens[self.index-2].name, self.tokens[self.index-1].name)
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
        elif self.is_word('{'):
            return self.block_()
        else:
            return self.assign()

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
        variable = self.next_token()
        self.match(';')
        return Decl(type_, variable)

    def assign(self):
        variable = self.next_token()
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
            operator = self.next_token().name
            expr = Arith(expr, self.term(), operator)
        return expr

    def term(self):
        expr = self.unary()

        while self.is_word('*') or self.is_word('/'):
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
        else:
            # 标识符
            t = self.next_token()
            return t
