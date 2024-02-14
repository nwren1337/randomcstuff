#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "include/bst.h"

int RAND_CAP = 1073741824;

int get_rand(int min, int max){
    return (rand() % max) + min;
}

btnode* insert_random_nums(btnode* root, int count) {
    int midpoint = RAND_CAP / 2; // this should result in clean division because we are working with powers of 2
    int r = midpoint;
    int inserted = 1;
    bool higher = false;
    root = insert(root, r);
    while (inserted <= count) {
        if(higher) {
            r = get_rand(midpoint + 1, RAND_CAP);
        } else {
            r = get_rand(0, midpoint - 1);
        }
        if(find(root, r) == NULL) {
            insert(root, r);
            inserted++;
            higher = !higher;
        }
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
        r = get_rand(0, RAND_CAP);
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
    for(int i = 128; i <= max_searches; i *= step) {
        start_clock = clock();
        search_for_random_nums(root, i);
        end_clock = clock();
        emit_result(i, end_clock - start_clock);
    }
}

btnode* test_random_insertion(btnode* root, int max_nodes) {
    int step = 2;
    clock_t start_clock, end_clock = 0;
    for(int i = 268435456; i <= max_nodes; i *= step) {
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
    int num_nodes = 268435456; // 2^28
    int num_searches = 134217728; //2^27
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

    // printf("  \"Sequential Insertion\": {\n");
    // seq_tree = test_sequential_insertion(seq_tree, num_nodes);
    // printf("  },\n");
    // printf("  \"Searching the sequential tree\": {\n" );
    // test_search(seq_tree, num_searches);
    // printf("  }\n}\n");
    // free_tree(seq_tree);

    return 0;
}