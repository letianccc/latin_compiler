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
        self.index_forward()
        return t

    def last_token(self):
        return self.tokens[self.index-1]

    def index_forward(self):
        self.index += 1

    def return_token(self):
        self.index += 1

    def match(self, word):
        name = self.next_token().name
        if name != word:
            print('not match!',
            'last:  ', self.tokens[self.index-2].name)
            print(self.index-1, name, word)
            raise Exception

    def block_(self):
        if self.is_word('{'):
            self.match('{')
            block = self.stmts_()
            self.match('}')
        else:
            block = self.stmts_()
        return block

    def stmts_(self):
        stmt = self.stmt_()
        if not self.is_word('}'):
            next_stmt = self.stmts_()
            stmt = Seq(stmt, next_stmt)
        return stmt

    def stmt_(self):
        t = self.cur_token()
        name = t.name
        if self.is_word('if'):
            self.match('if')
            self.match('(')
            cond = self.bool_()
            self.match(')')
            then_stmts = self.block_()
            return If(cond, then_stmts)
        elif self.is_word('int') or self.is_word('float'):
            return self.decl()
        else:
            return self.assign()

    def decl(self):
        type_ = self.next_token().name
        variable = self.next_token()
        self.match(';')
        return Decl(type_, variable)

    def assign(self):
        variable = self.next_token()
        self.match('=')
        value = self.next_token()
        self.match(';')
        return Assign(variable, value)

    def bool_(self):
        expr = self.join()
        if self.is_word('||'):
            self.match('||')
            expr = Or(expr, self.bool_())
        return expr

    def join(self):
        expr = self.equal()
        if self.is_word('&&'):
            self.match('&&')
            expr = And(expr, self.join())
        return expr

    def equal(self):
        expr = self.rel()

        if self.is_word('==') or self.is_word('!='):
            operator = self.next_token().name
            expr = Equal(expr, self.equal(), operator)
        return expr

    def rel(self):
        expr = self.expr_()

        if self.is_word('<') or self.is_word('<=') or self.is_word('>') or self.is_word('>='):
            operator = self.next_token().name
            expr = Rel(expr, self.expr_(), operator)
        return expr

    def expr_(self):
        expr = self.term()

        if self.is_word('+') or self.is_word('-'):
            operator = self.next_token().name
            expr = Arith(expr, self.term(), operator)
        return expr

    def term(self):
        expr = self.unary()

        if self.is_word('*') or self.is_word('/'):
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
