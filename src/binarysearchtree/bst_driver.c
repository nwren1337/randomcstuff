#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "bst/bst.h"

int RAND_CAP = 1000000;

int get_rand(){
    return rand() % RAND_CAP;
}

btnode* insert_random_nums(btnode* root, int count) {
    int r = get_rand();
    root = insert(root, r);
    for(int i = 1; i < count; i++) {
        r = get_rand();
        insert(root, r);
    }
    return root;
}

btnode* insert_sequential_nums(btnode* root, int count) {
    root = insert(root, 0);
    for(int i = 1; i < count; i++){
        insert(root, i);
    } 
    return root;
}

void search_for_random_nums(btnode* root, int count) {
    int searched = 0;
    int r = 0;
    while(searched < count) {
        r = get_rand();
        find(root, r); //return can be ignored, time to complete is what we are testing
        searched++;
    }
}

void emit_result(int num, long double elapsed) {
    printf("    \"%i\" : %Lf, \n", num, elapsed / (long double) CLOCKS_PER_SEC);
}

void test_search(btnode* root, int max_searches) {
    int step = 2;
    clock_t start_clock, end_clock = 0;
    for(int i = 1; i <= max_searches; i *= step) {
        start_clock = clock();
        search_for_random_nums(root, i);
        end_clock = clock();
        emit_result(i, end_clock - start_clock);
    }
}

btnode* test_random_insertion(btnode* root, int max_nodes) {
    int step = 2;
    clock_t start_clock, end_clock = 0;
    for(int i = 1; i <= max_nodes; i *= step) {
        free_tree(root);
        root = NULL;
        start_clock = clock();
        root = insert_random_nums(root, i);
        end_clock = clock();
        emit_result(i, end_clock - start_clock);
    }

    return root;
}

btnode* test_sequential_insertion(btnode* root, int max_nodes) {
    int step = 2;
    clock_t start_clock, end_clock = 0;
    for(int i = 1; i <= max_nodes; i *= step) {
        free_tree(root);
        root = NULL;
        start_clock = clock();
        root = insert_sequential_nums(root, i);
        end_clock = clock();
        emit_result(i, end_clock - start_clock);
    }

    return root;
}


int main() {
    /* Test setup */
    srand(time(NULL));
    int num_nodes = 131072; // 2^17 seems to be the most sequential insert can handle here
    int num_searches = 32768;
    btnode* random_tree = NULL;
    btnode* seq_tree = NULL;

    /* Random insertion tests */

    printf("{\n  \"Random Insertion\" : {\n");
    random_tree = test_random_insertion(random_tree, num_nodes);
    printf("  },\n");
    printf("  \"Searching the random tree\": {\n" );
    test_search(random_tree, num_searches);
    printf("  },\n");
    free_tree(random_tree);

    /* Sequential insertion tests */

    printf("  \"Sequential Insertion\": {\n");
    seq_tree = test_sequential_insertion(seq_tree, num_nodes);
    printf("  },\n");
    printf("  \"Searching the sequential tree\": {\n" );
    test_search(seq_tree, num_searches);
    printf("  }\n}\n");
    free_tree(seq_tree);

    return 0;
}