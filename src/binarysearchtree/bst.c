#include <stdlib.h>
#include "bst.h"

typedef struct binary_tree_node {
    int val;
    btnode* left;
    btnode* right;
} btnode;

size_t btnode_size(void) {
    return sizeof(btnode);
}

btnode* new_node(int value) {
    btnode* temp = (btnode*)malloc(btnode_size());
    temp->val = value;
    temp->left = temp->right = NULL;
    return temp;
}

int free_tree(btnode* root) {
    //BAD THIS ONLY "WORKS" BECAUSE WE CAN'T INSERT YET
    free(root);
    return 0;
}