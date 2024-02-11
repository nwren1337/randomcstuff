#include <stddef.h>
#include <stdbool.h>

/* avl.h */

/*********************************************************************
    Implements a binary search tree to the folling invariant :
        1. All tree nodes are binary nodes with two references
        2. All nodes of the left subtree are less than the root node
        3. All nodes of the right subtree are greater than the root
    This gives O(log n) runtime for insertion, search, and deletion operations
**********************************************************************/

/* opaque type definition */
typedef struct avl_tree_node avlnode;

/* utility func for malloc */
size_t avlnode_size(void);

/* getter for opaque typedef */
int get(avlnode* node);

/* CRUD operations */
avlnode* new_node(int val);

avlnode* find(avlnode* root, int target);

avlnode* insert(avlnode* root, int val);

avlnode* remove_node(avlnode* root, int target);

/* traversals */
void print_post_order(avlnode* root);

void print_in_order(avlnode* root);

void print_pre_order(avlnode* root);

avlnode* find_min(avlnode* root);

/* cleanup */
void free_tree(avlnode* root);