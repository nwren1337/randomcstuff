#include <stddef.h>
#include <stdbool.h>

/* bst.h */

/*********************************************************************
    Implements a binary search tree to the folling invariant :
        1. All tree nodes are binary nodes with two references
        2. All nodes of the left subtree are less than the root node
        3. All nodes of the right subtree are greater than the root
    This gives O(log n) runtime for insertion, search, and deletion operations
**********************************************************************/

/* opaque type definition */
typedef struct binary_tree_node btnode;

/* utility func for malloc */
size_t btnode_size(void);

/* getter for opaque typedef */
int get(btnode* node);

/* CRUD operations */
btnode* new_node(int val);

btnode* find(btnode* root, int target);

btnode* insert(btnode* root, int val);

btnode* remove_node(btnode* root, int target);

/* traversals */
void print_post_order(btnode* root);

void print_in_order(btnode* root);

void print_pre_order(btnode* root);

btnode* find_min(btnode* root);

/* cleanup */
void free_tree(btnode* root);