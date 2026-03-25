void insertionSort(int arr[], int n) {
    // starting from the second element
    for(int i = 1; i < n; i++) {
        int key = arr[i];
        // look at the previous element
        int j = i - 1;

        // shift elements of arr[0..i-1], that are greater than key, to one position ahead
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        // place the key in its correct position
        arr[j + 1] = key;
    }
}

void merge(int arr[], int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    // create temp arrays
    int L[n1], R[n2];

    // copy data to temp arrays
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];
    
    // merge the temp arrays back into arr[l..r]
    i = 0; j = 0; k = l;
    while (i < n1 && j < n2) {
        // compare the current elements of both arrays and add the smaller one to the merged array
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        // move to the next position in the merged array
        k++;
    }

    // copy the remaining elements of L[], if there are any
    while(i < n1) {
        arr[k] = L[i];
        i++; k++;
    }

    // copy the remaining elements of R[], if there are any
    while(j < n2) {
        arr[k] = R[j];
        j++; k++;
    }
}

void mergeSort(int arr[], int l, int r) {
    if (l < r ) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        merge(arr, l, m, r);
    }
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Lomuto partition scheme
int partition(int arr[], int low, int high) {
    // choose the last element as pivot
    int pivot = arr[high];

    // index of smaller element
    int i = low - 1;

    // iterate through the array and compare each element with the pivot
    for (int j = low; j < high; j++) {
        // if the current element is smaller than the pivot, swap it with the element at index i
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    // swap the pivot element with the element at index i + 1
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        // partition the array and get the pivot index
        int p1 = partition(arr, low, high);

        // recursively sort the elements before and after the partition
        quickSort(arr, low, p1 - 1);
        quickSort(arr, p1 + 1, high);
    }
}