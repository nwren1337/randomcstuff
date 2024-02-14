#include <stdlib.h>
#include <stdio.h>
#include "include/bst.h"

typedef struct binary_tree_node {
    int val;
    btnode* left;
    btnode* right;
} btnode;

size_t btnode_size(void) {
    return sizeof(btnode);
}

int get(btnode* node) {
    return node->val;
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

btnode* find(btnode* root, int target) {
    btnode* tmp = root;
    while(tmp != NULL) {
        if(target == tmp->val) {
            return tmp;
        } else if (target < tmp->val) {
            tmp = tmp->left;
        } else {
            tmp = tmp->right;
        }
    }
    return tmp; 
}

bool is_leaf(btnode* node) {
    if(node != NULL) {
        return (node->left == NULL) && (node->right == NULL);
    }
    return true;
}

bool single_child(btnode* node) {
    if(node != NULL) {
        return (node->left == NULL && node->right != NULL) || 
               (node->left != NULL && node->right == NULL);
    }
    return false;
}

btnode* find_min(btnode* root) {
    if(root != NULL) {
        if (root->left != NULL) {
            return find_min(root->left);
        }
    }
    return root;
}

btnode* remove_node(btnode* root, int target) {
    //guard against null
    if(root != NULL) {
        //recurse to target
        if(target < root->val) {
            root->left = remove_node(root->left, target);
        } else if(target > root->val) {
            root->right = remove_node(root->right, target);
        } else {
            //we are at our target
            //if the target is a leaf remove the node and return NULL
            if(is_leaf(root)) {
                free(root);
                return NULL;
            }
            //if the target has a single child, replace the target with the child and return it
            else if(single_child(root)) {
                btnode* temp;
                if (root->left != NULL) {
                    temp = root->left;
                } else {
                    temp = root->right;
                }
                free(root);
                return temp;
            }
            //if the target has two children
            else {
                // find the minimum node in the right subtree
                btnode* temp = find_min(root->right);
                //set this node to the minimum in the right
                root->val = temp->val;
                //remove the duplicate from the right subtree
                root->right = remove_node(root->right, temp->val);
            }
        }
    }
    return root;
}

void print_in_order(btnode* root) {
    if(root != NULL) {
        print_in_order(root->left);
        printf("%i ", root->val); 
        print_in_order(root->right);
    }
}

void print_post_order(btnode* root) {
    if(root != NULL) {
        print_in_order(root->left); 
        print_in_order(root->right);
        printf("%i ", root->val);
    }
}

void print_pre_order(btnode* root) {
    if(root != NULL) {
        printf("%i ", root->val); 
        print_in_order(root->left);
        print_in_order(root->right);
    }
}

void free_tree(btnode* root) {
    if (root != NULL) {
        free_tree(root->left);
        free_tree(root->right);
        free(root);
    }
}