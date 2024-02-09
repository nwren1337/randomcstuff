#include <stdio.h>
#include "bst.h"

int main() {
    btnode* node = NULL;
    node = insert(node, 5);
    insert(node, 3);
    insert(node, 4);
    insert(node, 8);
    insert(node, 10);
    print_in_order(node);
    printf("Cool.\n");
    free_tree(node);
    return 0;
}