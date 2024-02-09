#include <stdio.h>
#include "bst.h"

int main() {
    btnode* node = new_node(5);
    if(free_tree(node) == 0) {
        printf("Cool.\n");
    }
    return 0;
}