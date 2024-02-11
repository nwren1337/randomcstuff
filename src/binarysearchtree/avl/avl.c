#include "avl.h"

typedef struct avl_tree_node {
    int val;
    avnode* left;
    avnode* right;
    int height;
} avnode;