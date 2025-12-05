.section .text
.global _start

_startt:
    mov rdi, 0x4018b5
    mov rcx, 24
    mov rsi, 0x41

decrypt_loop:
    xor byte ptr [rdi], sil
    inc rdi
    loop decrypt_loop

    call _start
