#include <stdlib.h>
#include <stdio.h>
#include "include/avl.h"

typedef struct avl_tree_node {
    int val;
    avlnode* left;
    avlnode* right;
    int height;
} avlnode;

size_t avlnode_size(void) {
    return sizeof(avlnode);
}

int max(int a, int b) {
    return (a > b) ? a : b;
}


int get(avlnode* node) {
    return node->val;
}

int height(avlnode* node) {
    if(node == NULL) return 0;
    return node->height;
}

int balance(avlnode* node) {
    if(node == NULL) return 0;
    return height(node->left) - height(node->right);
}

avlnode* new_node(int value) {
    avlnode* temp = (avlnode*)malloc(avlnode_size());
    temp->val = value;
    temp->height = 0;
    temp->left = temp->right = NULL;
    return temp;
}

static avlnode* rotate_left(avlnode* root) {
    avlnode* y = root->right;
    avlnode* z = y->left;

    // Perform rotation
    y->left = root;
    root->right = z;

    // Update heights
    root->height = max(height(root->left), height(root->right)) + 1;
    y->height = max(height(y->left), height(y->right)) + 1;

    // Return new root
    return y;
}

static avlnode* rotate_right(avlnode* root) {
    avlnode* y = root->left;
    avlnode* z = y->right;

    // Perform rotation
    y->right = root;
    root->left = z;

    // Update heights
    root->height = max(height(root->left), height(root->right)) + 1;
    y->height = max(height(y->left), height(y->right)) + 1;

    // Return new root
    return y;
}

avlnode* insert(avlnode* root, int val) {
    if(root == NULL) return new_node(val);

    if(val < root->val) root->left = insert(root->left, val);
    else if (val > root->height) root->right = insert(root->right, val);
    else return root;

    root->height = 1 + max(height(root->left), height(root->right));

    int bal = balance(root);

    if(bal > 1 && val < root->left->val) return rotate_right(root);
    if(bal < -1 && val > root->right->val) return rotate_left(root);

    if(bal > 1 && val > root->left->val) {
        root->left = rotate_left(root);
        return rotate_right(root);
    }

    if(bal < -1 && val < root->right->val) {
        root->right = rotate_right(root);
        return rotate_left(root);
    }

    return root;
    
}

void print_in_order(avlnode* root) {
    if(root != NULL) {
        print_in_order(root->left);
        printf("%i ", root->val); 
        print_in_order(root->right);
    }
}

void print_post_order(avlnode* root) {
    if(root != NULL) {
        print_in_order(root->left); 
        print_in_order(root->right);
        printf("%i ", root->val);
    }
}

void print_pre_order(avlnode* root) {
    if(root != NULL) {
        printf("%i ", root->val); 
        print_in_order(root->left);
        print_in_order(root->right);
    }
}

void free_tree(avlnode* root) {
    if (root != NULL) {
        free_tree(root->left);
        free_tree(root->right);
        free(root);
    }
}