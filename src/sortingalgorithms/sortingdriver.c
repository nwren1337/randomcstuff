#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "include/sorting.h"

void printArray(int arr[], int size) {
    printf("[");
    for (int i = 0; i < size; i++) {
        printf("%d", arr[i]);
        if (i < size - 1) printf(", ");
    }
    printf("]\n");
}

void runSort(char alg, int arr[], int size) {
    switch (alg) {
        case 'i': insertionSort(arr, size);      break;
        case 'm': mergeSort(arr, 0, size - 1);   break;
        case 'q': quickSort(arr, 0, size - 1);   break;
        default:
            fprintf(stderr, "Unknown algorithm: %c\n", alg);
            return;
    }
}

int* readFile(char* filename, size_t* size) {
    FILE* f = fopen(filename, "rb");
    if (!f) {
        perror(filename);
        return NULL;
    }

    fseek(f, 0, SEEK_END);
    *size = ftell(f) / sizeof(int);
    rewind(f);

    int* arr = malloc(*size * sizeof(int));
    if (!arr) {
        perror("malloc");
        fclose(f);
        return NULL;
    }

    size_t read = fread(arr, sizeof(int), *size, f);
    if (read != *size) {
        fprintf(stderr, "%s: expected %zu elements, got %zu\n", filename, *size, read);
        free(arr);
        fclose(f);
        return NULL;
    }

    fclose(f);
    return arr;
}

int main(int argc, char* argv[]) {
    char algorithm = 0;
    int quiet = 0;
    int opt;

    while ((opt = getopt(argc, argv, "a:q")) != -1) {
        switch (opt) {
            case 'a':
                if (algorithm) {
                    fprintf(stderr, "Error: -a may only be specified once\n");
                    return 1;
                }
                if (optarg[0] != 'i' && optarg[0] != 'm' && optarg[0] != 'q') {
                    fprintf(stderr, "Error: -a argument must be i, m, or q\n");
                    return 1;
                }
                algorithm = optarg[0];
                break;
            case 'q': quiet = 1; break;
            default:
                fprintf(stderr, "Usage: %s -a [i|m|q] [-q] <filename>\n", argv[0]);
                return 1;
        }
    }

    if (!algorithm) {
        fprintf(stderr, "Error: algorithm required (-a [i|m|q])\n");
        return 1;
    }

    if (optind >= argc) {
        fprintf(stderr, "Error: filename required\n");
        return 1;
    }

    char* filename = argv[optind];

    size_t size;
    int* arr = readFile(filename, &size);
    if (!arr) return 1;

    if (!quiet) { printf("Before:\n"); printArray(arr, size); }
    runSort(algorithm, arr, size);
    if (!quiet) { printf("After:\n");  printArray(arr, size); }

    free(arr);
    return 0;
}