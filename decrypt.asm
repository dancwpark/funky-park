.section .text
.global _start

_start:
    mov rdi, 0x401775
    mov rcx, 24
    mov rsi, 0x41

decrypt_loop:
    xor byte ptr [rdi], sil
    inc rdi
    loop decrypt_loop

    movabs rax, 0x401650
    jmp rax
    

