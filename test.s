.section .rodata
.LC0:
.string "%d\n"
.text
.globl main
.type	main, @function
main:
pushq %rbp
movq	%rsp, %rbp
subq $120, %rsp
movq %fs:40, %rax
movq %rax, -8(%rbp)
xorl %eax, %eax
movl $45, -120(%rbp)
movl $95, -116(%rbp)
movl $15, -112(%rbp)
movl $78, -108(%rbp)
movl $84, -104(%rbp)
movl $51, -100(%rbp)
movl $24, -96(%rbp)
movl $12, -92(%rbp)
movl $8, %edx
movl %edx, -88(%rbp)
movl $0, %edx
movl %edx, -80(%rbp)
.L1:
movl -80(%rbp), %edx
movl -88(%rbp), %eax
subl $1, %eax
movl %eax, -72(%rbp)
cmpl -72(%rbp), %edx
jge .L2
movl $0, %edx
movl %edx, -84(%rbp)
.L3:
movl -84(%rbp), %edx
movl -88(%rbp), %eax
subl $1, %eax
movl %eax, -68(%rbp)
movl -68(%rbp), %eax
subl -80(%rbp), %eax
movl %eax, -64(%rbp)
cmpl -64(%rbp), %edx
jge .L4
movl -84(%rbp), %ecx
cltq
movl -120(%rbp, %rcx, 4), %edx
movl -84(%rbp), %eax
addl $1, %eax
movl %eax, -60(%rbp)
movl -60(%rbp), %ecx
cltq
cmpl -120(%rbp, %rcx, 4), %edx
jle .L5
movl -84(%rbp), %ecx
cltq
movl -120(%rbp, %rcx, 4), %edx
movl %edx, -76(%rbp)
movl -84(%rbp), %eax
addl $1, %eax
movl %eax, -56(%rbp)
movl -56(%rbp), %ecx
cltq
movl -120(%rbp, %rcx, 4), %edx
movl -84(%rbp), %ecx
cltq
movl %edx, -120(%rbp, %rcx, 4)
movl -76(%rbp), %edx
movl -84(%rbp), %eax
addl $1, %eax
movl %eax, -52(%rbp)
movl -52(%rbp), %ecx
cltq
movl %edx, -120(%rbp, %rcx, 4)
.L5:
movl -84(%rbp), %eax
addl $1, %eax
movl %eax, -48(%rbp)
movl -48(%rbp), %edx
movl %edx, -84(%rbp)
jmp .L3
.L4:
movl -80(%rbp), %eax
addl $1, %eax
movl %eax, -44(%rbp)
movl -44(%rbp), %edx
movl %edx, -80(%rbp)
jmp .L1
.L2:
movl $0, %edx
movl %edx, -84(%rbp)
.L6:
movl -84(%rbp), %edx
cmpl -88(%rbp), %edx
jge .L7
movl -84(%rbp), %ecx
cltq
movl -120(%rbp, %rcx, 4), %esi
movl $.LC0, %edi
movl $0, %eax
call printf
movl $0, %eax
movl -84(%rbp), %eax
addl $1, %eax
movl %eax, -40(%rbp)
movl -40(%rbp), %edx
movl %edx, -84(%rbp)
jmp .L6
.L7:
movq -8(%rbp), %rdx
xorq %fs:40, %rdx
je	.L8
call __stack_chk_fail
.L8:
leave
ret
.size	main, .-main
.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.6) 5.4.0 20160609"
.section	.note.GNU-stack,"",@progbits
