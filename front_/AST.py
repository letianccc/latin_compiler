class Block:
    def __init__(self, stmts):
        self.stmts = stmts

class Seq:
    def __init__(self, stmt, next_stmt):
        self.stmt = stmt
        self.next_stmt = next_stmt

class Stmt:
    def __init__(self, stmt):
        self.stmt = stmt

class If:
    def __init__(self, cond, then_stmts, else_stmts):
        self.cond = cond
        self.then = then_stmts
        self.else_ = else_stmts

class While:
    def __init__(self, cond, suite):
        self.cond = cond
        self.suite = suite

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.operator = '||'

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.operator = '&&'

class Equal:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

class Rel:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

class Arith:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

class Unary:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class Decl:
    def __init__(self, type_, variable):
        self.type_ = type_
        self.variable = variable

class Assign:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
