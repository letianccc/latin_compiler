.section	.rodata
.LC0:
.string	"%d\n"
.text
.globl main
.type	main, @function

main:
pushq %rbp
movq	%rsp, %rbp
movl $2, %eax
movl %eax, -4(%rbp)
movl $4, %eax
movl %eax, -8(%rbp)
cmpl $1, -4(%rbp)
jl .L1
cmpl $2, -8(%rbp)
jle .L4
cmpl $3, -4(%rbp)
jle .L1
.L4:
cmpl $2, -4(%rbp)
jge .L5
cmpl $3, -8(%rbp)
je .L2
.L5:
cmpl $2, -8(%rbp)
jne .L2
.L1:
movl $2, %eax
movl %eax, -12(%rbp)
jmp .L3
.L2:
movl $3, %eax
movl %eax, -12(%rbp)
.L3:
movl	%eax, %esi
movl	$.LC0, %edi
movl	$0, %eax
call	printf
movl	$0, %eax
leave
ret

.size	main, .-main
.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.6) 5.4.0 20160609"
.section	.note.GNU-stack,"",@progbits
