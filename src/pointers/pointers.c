#include <stdio.h>

int main() {
    int num = 69;
    int* num_ptr = &num;
     

    printf("Pointers are fun!\n");
    printf("value of our variable : %i (nice)\n", num);
    printf("value of our pointer: %p\n", num_ptr);
    printf("value of the value at our pointer: %i\n", *num_ptr);

    int num2 = 420;
    num_ptr = (num_ptr + 1);
    num_ptr = &num2;

    printf("value of our variable : %i\n", num2);
    printf("value of our pointer: %p\n", num_ptr);
    printf("value of the value at our pointer: %i\n", *num_ptr);

    printf("lets go backwards!\n");

    num_ptr = (num_ptr - 1);

    printf("value of our pointer: %p\n", num_ptr);
    printf("value of the value at our pointer: %i\n", *num_ptr);

    return 0;
}

