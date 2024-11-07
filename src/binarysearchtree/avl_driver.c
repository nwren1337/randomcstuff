#include "include/avl.h"

int main() {
    avlnode* test = NULL;
    for(int i = 0; i<10; i++) {
        test = insert(test, i);
    }
    print_in_order(test);
    free_tree(test);
    return 0;
}