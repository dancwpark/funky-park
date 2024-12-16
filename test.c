#include <stdio.h>

int add(int x, int y) {
    return x + y;
}

int main() {
    printf("Hello, World\n");
    int c = add(5, 4);
    printf("%d\n", c);
    return 0;
}
