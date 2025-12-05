# FUNKY PARK
Function packer with stub for runtime unpacking in python

Instead of encrypting a payload and appending it to a benign file, this project looks at encrypting functions in the target binary; no claims are made on benefit to evasion. 
This is specifically for making reverse engineering of any function somewhat more difficult; designed for creating simple CTF challenges. 

```ASM
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
```

The code snippet above is our decrypt blob. It is added to `.note` and the entrypoint for the binary is edited to
point to this blob. The addresses are currently hardcoded. `0x4018b5` is the function to be decrypted. `24` is the
size of the function. `0x41` is the key. At completion of decryption, the program redirects to `0x401790`, the original
`_start` function.

## TODO
* Do both 32 and 64 bit ELFs
* Do relocations so binary does not have to be statically compiled
* Make a wrapper to deal with managing addresses (get rid of hardcoded variables)
