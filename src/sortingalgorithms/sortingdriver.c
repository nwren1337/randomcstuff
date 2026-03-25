#include <stdio.h>
#include <string.h>
#include "include/sorting.h"

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void runSort(char* sortName, int arr[], int size) {
    printf("%s: \n", sortName);
    printf("Before: \n");
    printArray(arr, size);

    if (strcmp(sortName, "Insertion Sort") == 0) {
        insertionSort(arr, size);
    } else if (strcmp(sortName, "Merge Sort") == 0) {
        mergeSort(arr, 0, size - 1);
    } else if (strcmp(sortName, "Quick Sort") == 0) {
        quickSort(arr, 0, size - 1);
    } else {
        printf("Unknown sort function: %s\n", sortName);
        return;
    }

    printf("After: \n");
    printArray(arr, size);
}

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int size = sizeof(arr) / sizeof(arr[0]);

    runSort("Insertion Sort", arr, size);

    int arr2[] = {64, 34, 25, 12, 22, 11, 90}; 
    runSort("Merge Sort", arr2, size);

    int arr3[] = {64, 34, 25, 12, 22, 11, 90};
    runSort("Quick Sort", arr3, size);

    return 0;
}