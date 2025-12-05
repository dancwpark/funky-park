.section .text
.global _start

_start:
    mov rdi, 0x4018b5
    mov rcx, 24
    mov rsi, 0x41

decrypt_loop:
    xor byte ptr [rdi], sil
    inc rdi
    loop decrypt_loop

    movabs rax, 0x401790
    jmp rax
