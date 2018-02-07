def print_token_names(tokens):
    token_names = [t.name for t in tokens]
    print(token_names)

def insert_(ir):
    start =   '.section	.rodata\n'\
              '.LC0:\n'\
              '.string	"%d\\n"\n'\
              '.text\n'\
              '.globl main\n'\
              '.type	main, @function\n\n'\
              'main:\n'\
              'pushq %rbp\n'\
              'movq	%rsp, %rbp\n'

    end =     'movl	%eax, %esi\n'\
              'movl	$.LC0, %edi\n'\
              'movl	$0, %eax\n'\
              'call	printf\n'\
              'movl	$0, %eax\n'\
              'leave\n'\
              'ret\n\n'\
              '.size	main, .-main\n'\
              '.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.6) 5.4.0 20160609"\n'\
              '.section	.note.GNU-stack,"",@progbits\n'
    return start + ir + end
