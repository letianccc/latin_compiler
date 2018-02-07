
as_map = {'==' : 'je',
          '!=': 'jne',
          '<' : 'jl',
          '<=': 'jle',
          '>':  'jg',
          '>=': 'jge',
          }
as_reverse_map = {'==' : 'jne',
                  '!=': 'je',
                  '>=' : 'jl',
                  '>': 'jle',
                  '<=':  'jg',
                  '<': 'jge',
                  }

class Generator_as:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = list()
        self.symbol_map = dict()
        self.symbol_count = 1
        self.line_count = 1
        self.block_count = 1
        self.ir = ''
        # self.init_ir()
        self.gen(self.ast)
        # self.ir += 'L' + str(self.line_count) + ': End\n'
        # self.end_ir()

    def init_ir(self):
        self.ir = '.section	.rodata\n'\
                  '.LC0:\n'\
                  '.string	"OK"\n'\
                  '.text\n'\
                  '.globl main\n'\
                  '.type	main, @function\n'\
                  'main:\n'\
                  'pushq %rbp\n'\
                  'movq	%rsp, %rbp\n'

    def end_ir(self):
        self.ir += 'movl	$.LC0, %edi\n'\
                   'movl	$0, %eax\n'\
                   'call	puts\n'\
                   'movl	$0, %eax\n'\
                   'popq	%rbp\n'\
                   'ret\n'\
                   '.size	main, .-main\n'\
                   '.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.6) 5.4.0 20160609"\n'\
                   '.section	.note.GNU-stack,"",@progbits\n'

    def gen(self, node):
        if self.is_node_type(node, 'Seq'):
            self.gen(node.stmt)
            self.gen(node.next_stmt)
        elif self.is_node_type(node, 'Decl'):
            self.gen_decl(node)
        elif self.is_node_type(node, 'Assign'):
            self.gen_assign(node)
        elif self.is_node_type(node, 'If'):
            self.gen_if(node)
        elif self.is_node_type(node, 'While'):
            self.gen_while(node)
        elif node is None:
            return None

    def gen_decl(self, node):
        token = node.variable
        name = token.name
        self.symbol_table.append(name)
        self.symbol_map[name] = self.symbol_count
        self.symbol_count += 1

    def gen_assign(self, node):
        name = node.variable.name
        left = self.addr(self.symbol_map[name])
        right = self.gen_expr(node.value)
        # 加减乘除返回%eax
        ir1 = 'movl ' + right + ', ' + '%eax' + '\n'
        ir2 = 'movl ' + '%eax' + ', ' + left + '\n'
        ir = ir1 + ir2
        self.gen_ir(ir)

    def gen_expr(self, node):
        if self.is_node_type(node, 'Token'):
            if node.type_ == 'number':
                return '$' + node.name
            elif node.type_ == 'identifier':
                index = self.symbol_map[node.name]
                return self.addr(index)
        elif self.is_node_type(node, 'Arith'):
            return self.gen_arith(node)
        elif self.is_node_type(node, 'Unary'):
            return node.operator + self.gen_expr(node.operand)

    def gen_arith(self, node):
        left = self.gen_expr(node.left)
        right = self.gen_expr(node.right)
        ir1 = 'movl ' + left + ', ' + '%eax\n'
        ir2 = 'movl ' + right + ', ' + '%edx\n'

        op = node.operator
        if op == '+':
            op_as = 'addl'
        elif op == '-':
            op_as = 'subl'
        elif op == '*':
            op_as = 'imull'
        elif op == '/':
            op_as = 'idivl'
        # 除法暂时未实现
        # if op == '/':
        #     ir1 = 'movl ' + left + ', ' + '%eax\n'
        #     ir2 = 'cltd\n'
        #     ir3 = 'idivl ' + right + '\n'
        # else:
        ir3 = op_as + ' ' + '%edx, %eax\n'

        index = self.symbol_count
        self.symbol_count += 1
        addr_ = self.addr(index)
        ir4 = 'movl %eax, ' + addr_ + '\n'
        ir = ir1 + ir2 + ir3 + ir4
        self.gen_ir(ir)
        return addr_

    def addr(self, index):
        return '-' + str(index * 4) + '(%rbp)'

    # jump_style 决定 if false jump 或者 if true jump
    def gen_if(self, node):
        then_block = self.new_block()
        next_block = self.new_block()
        if node.else_:
            else_block = next_block
            extern_block = self.new_block()
        else:
            extern_block = next_block

        self.gen_cond(node.cond, then_block, next_block)
        self.gen_then(node, then_block, extern_block)
        if node.else_:
            self.gen_else(node, else_block)
        self.gen_tag_after_if(extern_block)

    def gen_cond(self, node, true_block, false_block):
        jump_style = False
        self.gen_logic(node, true_block, false_block, jump_style)

    def gen_then(self, node, then_block, extern_block):
        ir = self.block_flag(then_block)
        self.gen_ir(ir)
        self.gen(node.then)
        if node.else_:
            ir = 'jmp ' + extern_block + '\n'
            self.gen_ir(ir)

    def gen_else(self, node, else_block):
        ir = self.block_flag(else_block)
        self.gen_ir(ir)
        self.gen(node.else_)

    def gen_tag_after_if(self, extern_block):
        ir = self.block_flag(extern_block)
        self.gen_ir(ir)

    def gen_logic(self, node, true_block, false_block, jump_style):
        if self.is_node_type(node, 'Or'):
            self.gen_or(node, true_block, false_block, jump_style)
        elif self.is_node_type(node, 'And'):
            self.gen_and(node, true_block, false_block, jump_style)
        else:
            target = true_block if jump_style else false_block
            self.gen_cmp(node, target, jump_style)

    # 对于or表达式左边的逻辑判断块，如果为True，则跳转到true_block，如果为False,
    # 则会执行or右边的逻辑判断块。
    # 如果or的左子树以及左子树的右子树为And类，则需要产生新的块标签，表示or右边的逻辑块，
    # 并且将传递给子函数的false_block修改为新的块标签，而不是or的false_block
    # 因为And表达式左边如果为False，会执行跳转语句，跳过And右边的代码块，跳转到or右边的代码块。
    # 因此And使用的false_block应该为or右边的代码块
    # 否则，在表达式为False时，or的左边会顺序执行代码，不需要跳转到false_block，
    # 因此将false_block设置为None。
    # and表达式同理。
    def gen_or(self, node, true_block, false_block, jump_style):
        left_jump_style = True
        right_jump_style = jump_style
        left = node.left
        right_of_left = left.right
        need_new_block = self.is_node_type(left, 'And') \
                        or self.is_node_type(right_of_left, 'And')
        if need_new_block:
            right_block = self.new_block()
            self.gen_logic(node.left, true_block, right_block, left_jump_style)
            ir = self.block_flag(right_block)
            self.gen_ir(ir)
        else:
            self.gen_logic(node.left, true_block, None, left_jump_style)
        self.gen_logic(node.right, true_block, false_block, right_jump_style)

    def gen_and(self, node, true_block, false_block, jump_style):
        left_jump_style = False
        right_jump_style = jump_style
        left = node.left
        left_right = left.right
        need_new_block = self.is_node_type(left, 'Or') \
                        or self.is_node_type(left_right, 'Or')
        if need_new_block:
            right_block = self.new_block()
            self.gen_logic(node.left, right_block, false_block, left_jump_style)
            ir = self.block_flag(right_block)
            self.gen_ir(ir)
        else:
            self.gen_logic(node.left, None, false_block, left_jump_style)
        self.gen_logic(node.right, true_block, false_block, right_jump_style)

    def gen_cmp(self, node, target_block, jump_style):
        self.gen_cmp_stmt(node)
        self.gen_jump(node.operator, target_block, jump_style)

    def gen_cmp_stmt(self, node):
        left = self.gen_expr(node.left)
        right = self.gen_expr(node.right)
        ir = 'cmpl ' + right + ', ' + left + '\n'
        self.gen_ir(ir)

    def gen_jump(self, cmp_operator, target_block, jump_style):
        if jump_style == True:
            jmp_ir = as_map[cmp_operator]
        else:
            jmp_ir = as_reverse_map[cmp_operator]
        ir = jmp_ir + ' ' + target_block + '\n'
        self.gen_ir(ir)

    def gen_ir(self, ir):
        self.ir += ir

    def new_block(self):
        c = self.block_count
        self.block_count += 1
        block_tag = '.L' + str(c)
        return block_tag

    def block_flag(self, block_tag):
        return block_tag + ':' + '\n'

    def is_node_type(self, node, type_):
        return node.__class__.__name__ == type_

class Generator:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = list()
        self.symbol_map = dict()
        self.symbol_count = 0
        self.line_count = 1
        self.ir = ''
        self.gen(self.ast)
        self.ir += 'L' + str(self.line_count) + ': End\n'

    def cur_line_flag(self):
        return 'L' + str(self.line_count) + ': '

    def cur_line(self):
        return 'L' + str(self.line_count)

    def next_line(self):
        self.line_count += 1

    def gen(self, node):
        if self.is_node_type(node, 'Seq'):
            self.gen(node.stmt)
            self.gen(node.next_stmt)
        elif self.is_node_type(node, 'Decl'):
            self.gen_decl(node)
        elif self.is_node_type(node, 'Assign'):
            self.gen_assign(node)
        elif self.is_node_type(node, 'If'):
            self.gen_if(node)
        elif self.is_node_type(node, 'While'):
            self.gen_while(node)
        elif node is None:
            return None

    def gen_while(self, node):
        first_while_line = self.cur_line()
        cond = self.gen_expr(node.cond)

        jump_index = len(self.ir)
        jump_line = self.cur_line_flag()
        self.next_line()

        suite = self.gen(node.suite)
        last_suite_ir = self.cur_line_flag() + 'goto ' + first_while_line + '\n'
        self.next_line()
        self.ir += last_suite_ir

        jump_line_ir = jump_line + 'if ' + cond + ' is false goto ' + self.cur_line() + '\n'
        self.ir = self.ir[:jump_index] + jump_line_ir + self.ir[jump_index:]

    def gen_if(self, node):
        cond = self.gen_expr(node.cond)
        jump_to_else_index = len(self.ir)
        jump_to_else__flag = self.cur_line_flag()
        self.next_line()

        then = self.gen(node.then)
        jump_to_extern_index = len(self.ir)
        jump_to_extern_flag = self.cur_line_flag()
        self.next_line()

        else_position = self.cur_line()
        else_ = self.gen(node.else_)
        extern_position = self.cur_line()

        jump_to_else_ir = jump_to_else__flag + 'if ' + cond + ' is false goto ' + else_position + '\n'
        jump_to_extern_ir = jump_to_extern_flag + 'goto ' + extern_position + '\n'
        jump_to_extern_index += len(jump_to_else_ir)
        self.ir = self.ir[:jump_to_else_index] + jump_to_else_ir + self.ir[jump_to_else_index:]
        self.ir = self.ir[:jump_to_extern_index] + jump_to_extern_ir + self.ir[jump_to_extern_index:]

    def gen_decl(self, node):
        token = node.variable
        name = token.name
        self.symbol_table.append(name)
        self.symbol_map[name] = 't' + str(self.symbol_count)
        self.symbol_count += 1

    def gen_assign(self, node):
        name = node.variable.name
        left = self.symbol_map[name]
        right = self.gen_expr(node.value)
        line = 'L' + str(self.line_count) + ': '
        ir = line + left + ' = ' + right + '\n'
        self.ir += ir
        self.line_count += 1

    def gen_expr(self, node):
        if self.is_node_type(node, 'Token'):
            if node.type_ == 'number':
                return node.name
            elif node.type_ == 'identifier':
                t = self.symbol_map[node.name]
                return t
        elif self.is_node_type(node, 'Arith') or \
                self.is_node_type(node, 'And') or \
                self.is_node_type(node, 'Or') or \
                self.is_node_type(node, 'Rel') or \
                self.is_node_type(node, 'Equal'):
            left = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            t = 't' + str(self.symbol_count)
            line = 'L' + str(self.line_count) + ': '
            ir = line + t + ' = ' + left + ' ' + node.operator + ' ' + right + '\n'
            self.ir += ir
            self.symbol_count += 1
            self.line_count += 1
            return t
        elif self.is_node_type(node, 'Unary'):
            return node.operator + self.gen_expr(node.operand)



    def is_node_type(self, node, type_):
        return node.__class__.__name__ == type_
