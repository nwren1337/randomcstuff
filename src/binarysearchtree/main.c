#include <stdio.h>
#include "bst.h"

int main() {
    /* Test insertion and printing */
    btnode* node = NULL;
    node = insert(node, 5);
    insert(node, 3);
    insert(node, 4);
    insert(node, 8);
    insert(node, 10);
    print_in_order(node);
    printf("\n");

    /* Test removing a single node */
    btnode* node2 = NULL;
    node2 = insert(node2, 5);
    insert(node2, 3);
    insert(node2, 6);
    print_in_order(node2); // 3 5 6
    printf("\n");
    //remove a leaf
    remove_node(node2, 3);
    print_in_order(node2); // 5 6
    printf("\n");
    //re-add a leaf
    insert(node2, 1);
    print_in_order(node2); // 1 5 6
    printf("\n");
    //remove the root
    remove_node(node2, 5);
    print_in_order(node2); // 1 6
    printf("\n");
    //set up subtree with single child to swap
    insert(node2, 7);
    insert(node2, 8);
    insert(node2, 9);
    print_in_order(node2); // 1 6 7 8 9
    printf("\n");
    remove_node(node2, 8);
    print_in_order(node2); // 1 6 7 9
    printf("\n");


    /* cleanup */
    free_tree(node);
    free_tree(node2);
    return 0;
}