#include <stdio.h>
#include <stdint.h>
#include <sys/mman.h>
#include <unistd.h>
#include <assert.h>

// version of test that includes decrypter IN
// the code to allow for compilation of dynamically linked
// binaries

int add(int x, int y) {
    return x + y;
}


int remove_prot(void *addr) {
    int size = getpagesize();
    addr -= (unsigned long)addr % size;

    if (mprotect(addr, size, PROT_READ | PROT_WRITE | PROT_EXEC) == -1) {
        return -1;
    }
    return 0;
}


void apply_prot(void *addr) {
    int size = getpagesize();
    addr -= (unsigned long)addr % size;
    assert(mprotect(addr, size, PROT_READ | PROT_EXEC) != -1);
}


int decrypt() {
    char key = 'A';
    int len_of_add = 24;
    void *ptr = &add;
    if (remove_prot(ptr) == -1) {
        return -1;
    }
    for (int i = 0; i < len_of_add; ++i) {
        //printf("%p\n", (char *)ptr);
        //printf("%hhu\n", *(char *)(ptr+i));
        int a = (*(char *)(ptr + i)) ^ 65;
        //printf("%x\n", a);
        //printf("%hhu\n", *(char *)(ptr+i));
        //printf("%02x\n", *(char *)(ptr+i));
        *(char *)(ptr + i) = a;
    }

    apply_prot(ptr);
    return 0;
}

int main() {
    printf("Hello, World\n");
    if (decrypt() == -1) {
        printf("dksf\n");
        return -1;
    }
    int c = add(5, 4);
    printf("%d\n", c);
    return 0;
}
