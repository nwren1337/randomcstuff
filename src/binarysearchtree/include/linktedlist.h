#include <stddef.h>
#include <stdbool.h>

typedef struct linked_list_node llnode;

/* utility func for malloc */
size_t llnode_size(void);

/* getter for opaque typedef */
int get(llnode* node);

/* CRUD */
llnode* new_node(int val);

llnode* search(llnode* root, int num);

llnode* add(llnode* root, int num);

llnode* append(llnode* root, int num);

llnode* remove(llnode* root, int target);

/* The dreaded reversal */

llnode* reverse(llnode* root);

/* Print */

void print_list(llnode* root);

/* cleanup */
void free_list(llnode* root);