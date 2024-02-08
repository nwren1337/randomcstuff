#include <stdio.h>

long factorial(int n) {
    if(n == 0) return 1;
    return n * factorial(n - 1);
}

int main() {
    int num = 20;
    printf("%li\n", factorial(num));
}

