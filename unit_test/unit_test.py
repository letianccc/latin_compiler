from front_.lexer_ import skip_space, scan_tok, lexer
from front_.parser_ import Parser
from util import *



def assert_type(node, type_):
    assert(node.__class__.__name__ == type_)

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
    assert (tokens[1].type_ == 'reserved')
    assert (tokens[2].name == 'a')
    assert (tokens[2].type_ == 'identifier')
    assert (tokens[3].name == ';')
    assert (tokens[3].type_ == 'symbol')
    assert (tokens[4].name == '}')
    assert (tokens[4].type_ == 'symbol')

    code = '{int abc123_a=1<=2;}'
    tokens = lexer(code)
    assert (tokens[0].name == '{')
    assert (tokens[0].type_ == 'symbol')
    assert (tokens[1].name == 'int')
    assert (tokens[1].type_ == 'reserved')
    assert (tokens[2].name == 'abc123_a')
    assert (tokens[2].type_ == 'identifier')
    assert (tokens[3].name == '=')
    assert (tokens[3].type_ == 'symbol')
    assert (tokens[4].name == '1')
    assert (tokens[4].type_ == 'number')
    assert (tokens[5].name == '<=')
    assert (tokens[5].type_ == 'symbol')
    assert (tokens[6].name == '2')
    assert (tokens[6].type_ == 'number')
    assert (tokens[7].name == ';')
    assert (tokens[7].type_ == 'symbol')
    assert (tokens[8].name == '}')
    assert (tokens[8].type_ == 'symbol')

    code = 'if (a<=1) a=1;'
    tokens = lexer(code)
    assert (tokens[0].name == 'if')
    assert (tokens[0].type_ == 'reserved')
    assert (tokens[1].name == '(')
    assert (tokens[1].type_ == 'symbol')
    assert (tokens[2].name == 'a')
    assert (tokens[2].type_ == 'identifier')
    assert (tokens[3].name == '<=')
    assert (tokens[3].type_ == 'symbol')
    assert (tokens[4].name == '1')
    assert (tokens[4].type_ == 'number')
    assert (tokens[5].name == ')')
    assert (tokens[5].type_ == 'symbol')
    assert (tokens[6].name == 'a')
    assert (tokens[6].type_ == 'identifier')
    assert (tokens[7].name == '=')
    assert (tokens[7].type_ == 'symbol')
    assert (tokens[8].name == '1')
    assert (tokens[8].type_ == 'number')
    assert (tokens[9].name == ';')
    assert (tokens[9].type_ == 'symbol')

    code = 'if (a<=1&&b==4) a=1;'
    tokens = lexer(code)
    assert (tokens[0].name == 'if')
    assert (tokens[0].type_ == 'reserved')
    assert (tokens[1].name == '(')
    assert (tokens[1].type_ == 'symbol')
    assert (tokens[2].name == 'a')
    assert (tokens[2].type_ == 'identifier')
    assert (tokens[3].name == '<=')
    assert (tokens[3].type_ == 'symbol')
    assert (tokens[4].name == '1')
    assert (tokens[4].type_ == 'number')
    assert (tokens[5].name == '&&')
    assert (tokens[5].type_ == 'symbol')
    assert (tokens[6].name == 'b')
    assert (tokens[6].type_ == 'identifier')
    assert (tokens[7].name == '==')
    assert (tokens[7].type_ == 'symbol')
    assert (tokens[8].name == '4')
    assert (tokens[8].type_ == 'number')
    assert (tokens[9].name == ')')
    assert (tokens[9].type_ == 'symbol')
    assert (tokens[10].name == 'a')
    assert (tokens[10].type_ == 'identifier')
    assert (tokens[11].name == '=')
    assert (tokens[11].type_ == 'symbol')
    assert (tokens[12].name == '1')
    assert (tokens[12].type_ == 'number')
    assert (tokens[13].name == ';')
    assert (tokens[13].type_ == 'symbol')

    code = 'if (a<=1&b==4) a=1;'
    tokens = lexer(code)
    assert (tokens[0].name == 'if')
    assert (tokens[0].type_ == 'reserved')
    assert (tokens[1].name == '(')
    assert (tokens[1].type_ == 'symbol')
    assert (tokens[2].name == 'a')
    assert (tokens[2].type_ == 'identifier')
    assert (tokens[3].name == '<=')
    assert (tokens[3].type_ == 'symbol')
    assert (tokens[4].name == '1')
    assert (tokens[4].type_ == 'number')
    assert (tokens[5].name == '&')
    assert (tokens[5].type_ == 'symbol')
    assert (tokens[6].name == 'b')
    assert (tokens[6].type_ == 'identifier')
    assert (tokens[7].name == '==')
    assert (tokens[7].type_ == 'symbol')
    assert (tokens[8].name == '4')
    assert (tokens[8].type_ == 'number')
    assert (tokens[9].name == ')')
    assert (tokens[9].type_ == 'symbol')
    assert (tokens[10].name == 'a')
    assert (tokens[10].type_ == 'identifier')
    assert (tokens[11].name == '=')
    assert (tokens[11].type_ == 'symbol')
    assert (tokens[12].name == '1')
    assert (tokens[12].type_ == 'number')
    assert (tokens[13].name == ';')
    assert (tokens[13].type_ == 'symbol')


def test_parser():
    code = '{int a;a=2;}'
    parser_case1(code)

    code = '{int a;a=2;int b;b=4;}'
    parser_case2(code)

    code = '{int a; a=2; a = a + 2 * 3 + 4;}'
    parser_case7(code)

    code = '{int a; a=2; int b; b=4; a = a + a * (2 + 3) + b;}'
    parser_case6(code)

    code = '{if(a==1)a=1;}'
    parser_case3(code)

    code = '{if(a==1){a=1;}}'
    parser_case4(code)

    code = '{if(a<=3&&b==4){int d;d=1;a=4;}k=4;d=2;}'
    parser_case5(code)

    code = '{int a;a=1;if(a==1)a=2;else a=3;}'
    case8(code)


def case9(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    root = parser.AST
    node = root

    cond = node.cond
    then = node.then
    else_ = node.else_

    assert(node.__class__.__name__ == 'If')
    assert(cond.__class__.__name__ == 'Equal')
    assert(cond.left.name == 'a')
    assert(cond.right.name == '1')
    assert(cond.operator == '==')
    assert(then.__class__.__name__ == 'Assign')
    assert(then.variable.name == 'a')
    assert(then.value.name == '2')
    assert(else_.__class__.__name__ == 'Assign')
    assert(else_.variable.name == 'a')
    assert(else_.value.name == '3')



def parser_case1(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    root = parser.AST
    node = root

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Decl')
    assert(stmt.type_ == 'int')
    assert(stmt.variable.name == 'a')
    node = node.next_stmt

    stmt = node
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'a')
    assert(stmt.value.name == '2')


def parser_case2(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    root = parser.AST
    node = root

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Decl')
    assert(stmt.type_ == 'int')
    assert(stmt.variable.name == 'a')
    node = node.next_stmt

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'a')
    assert(stmt.value.name == '2')
    node = node.next_stmt

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Decl')
    assert(stmt.type_ == 'int')
    assert(stmt.variable.name == 'b')
    node = node.next_stmt

    stmt = node
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'b')
    assert(stmt.value.name == '4')


def parser_case3(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    root = parser.AST
    cond = root.cond
    then = root.then
    else_ = root.else_
    assert(root.__class__.__name__ == 'If')
    assert(cond.__class__.__name__ == 'Equal')
    assert(cond.left.name == 'a')
    assert(cond.right.name == '1')
    assert(cond.operator == '==')
    assert(then.__class__.__name__ == 'Assign')
    assert(then.variable.name == 'a')
    assert(then.value.name == '1')
    assert(else_ == None)


def parser_case4(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    root = parser.AST
    cond = root.cond
    then = root.then
    assert(root.__class__.__name__ == 'If')
    assert(cond.__class__.__name__ == 'Equal')
    assert(cond.left.name == 'a')
    assert(cond.right.name == '1')
    assert(cond.operator == '==')
    assert(then.__class__.__name__ == 'Assign')
    assert(then.variable.name == 'a')
    assert(then.value.name == '1')






    # {if(a<=3&&b==4){int d=3;d=1;a=4;}k=4;d=2}


def parser_case5(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    root = parser.AST
    if_ = root.stmt
    assert(root.__class__.__name__ == 'Seq')
    assert(if_.__class__.__name__ == 'If')

    cond = if_.cond
    left = cond.left
    right = cond.right
    assert(cond.__class__.__name__ == 'And')
    assert(left.__class__.__name__ == 'Rel')
    assert(left.left.name == 'a')
    assert(left.right.name == '3')
    assert(left.operator == '<=')
    assert(right.__class__.__name__ == 'Equal')
    assert(right.left.name == 'b')
    assert(right.right.name == '4')
    assert(right.operator == '==')

    node = if_.then
    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Decl')
    assert(stmt.type_ == 'int')
    assert(stmt.variable.name == 'd')
    node = node.next_stmt

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'd')
    assert(stmt.value.name == '1')
    node = node.next_stmt

    stmt = node
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'a')
    assert(stmt.value.name == '4')

    node = root.next_stmt
    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'k')
    assert(stmt.value.name == '4')

    stmt = node.next_stmt
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'd')
    assert(stmt.value.name == '2')


def parser_case6(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    root = parser.AST
    node = root

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Decl')
    assert(stmt.type_ == 'int')
    assert(stmt.variable.name == 'a')
    node = node.next_stmt

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'a')
    assert(stmt.value.name == '2')
    node = node.next_stmt

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Decl')
    assert(stmt.type_ == 'int')
    assert(stmt.variable.name == 'b')
    node = node.next_stmt

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'b')
    assert(stmt.value.name == '4')
    node = node.next_stmt

    stmt = node
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'a')

    expr = stmt.value
    assert_type(expr, 'Arith')
    assert(expr.operator == '+')
    assert(expr.right.name == 'b')
    expr = expr.left
    assert_type(expr, 'Arith')
    assert(expr.operator == '+')
    assert(expr.left.name == 'a')
    expr = expr.right
    assert_type(expr, 'Arith')
    assert(expr.operator == '*')
    assert(expr.left.name == 'a')
    expr = expr.right
    assert_type(expr, 'Arith')
    assert(expr.operator == '+')
    assert(expr.left.name == '2')
    assert(expr.right.name == '3')


def parser_case7(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    root = parser.AST
    node = root

    stmt = node.stmt
    assert_type(node, 'Seq')
    assert_type(stmt, 'Decl')
    assert(stmt.type_ == 'int')
    assert(stmt.variable.name == 'a')
    node = node.next_stmt

    stmt = node.stmt
    assert_type(node, 'Seq')
    assert_type(stmt, 'Assign')
    assert(stmt.variable.name == 'a')
    assert(stmt.value.name == '2')
    node = node.next_stmt

    stmt = node
    assert_type(stmt, 'Assign')
    assert(stmt.variable.name == 'a')

    expr = stmt.value
    assert_type(expr, 'Arith')
    assert(expr.operator == '+')
    assert(expr.right.name == '4')
    expr = expr.left
    assert_type(expr, 'Arith')
    assert(expr.operator == '+')
    assert(expr.left.name == 'a')
    expr = expr.right
    assert_type(expr, 'Arith')
    assert(expr.operator == '*')
    assert(expr.left.name == '2')
    assert(expr.right.name == '3')

def case8(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    root = parser.AST
    node = root

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Decl')
    assert(stmt.type_ == 'int')
    assert(stmt.variable.name == 'a')
    node = node.next_stmt

    stmt = node.stmt
    assert(node.__class__.__name__ == 'Seq')
    assert(stmt.__class__.__name__ == 'Assign')
    assert(stmt.variable.name == 'a')
    assert(stmt.value.name == '1')
    node = node.next_stmt

    cond = node.cond
    then = node.then
    else_ = node.else_

    assert(node.__class__.__name__ == 'If')
    assert(cond.__class__.__name__ == 'Equal')
    assert(cond.left.name == 'a')
    assert(cond.right.name == '1')
    assert(cond.operator == '==')
    assert(then.__class__.__name__ == 'Assign')
    assert(then.variable.name == 'a')
    assert(then.value.name == '2')
    assert(else_.__class__.__name__ == 'Assign')
    assert(else_.variable.name == 'a')
    assert(else_.value.name == '3')




test_scan_tok()
test_lexer()
test_parser()
