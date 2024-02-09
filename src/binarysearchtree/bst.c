#include <stdlib.h>
#include <stdio.h>
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

btnode* insert(btnode* root, int val) {
    if(root == NULL) return new_node(val);
    if(val < root->val) root->left = insert(root->left, val);
    if(val > root->val) root->right = insert(root->right, val);
    return root;
}

void print_in_order(btnode* root) {
    if(root != NULL) {
        print_in_order(root->left);
        printf(" %i ", root->val); 
        print_in_order(root->right);
    }
}

int free_tree(btnode* root) {
    //BAD THIS ONLY "WORKS" BECAUSE WE CAN'T INSERT YET
    free(root);
    return 0;
}