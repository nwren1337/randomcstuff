import numpy as np
import argparse

arg = argparse.ArgumentParser(description="Implementations of sorting algorithms.")
arg.add_argument("file", type=str, help="Path to the binary file containing the array to sort.")
arg.add_argument("--algorithm", type=str, choices=["insertion", "quick", "merge"], default="merge", help="Sorting algorithm to use (default: merge).")
arg.add_argument("--quiet", action="store_true", help="Suppress output of the sorted array.")

def insertion_sort(arr: list[int]) -> None:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def pivot(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]  # choose the last element as pivot
    i = low - 1  # index of smaller element

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1  # increment index of smaller element
            arr[i], arr[j] = arr[j], arr[i]  # swap

    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # swap pivot into correct position
    return i + 1

def quick_sort(arr: list[int], low: int, high: int) -> None:
    if low < high:
        pi = pivot(arr, low, high)  # partitioning index
        quick_sort(arr, low, pi - 1)  # recursively sort elements before partition
        quick_sort(arr, pi + 1, high)  # recursively sort elements after partition

def merge(arr: list[int], l: int, m: int, r: int) -> None:
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = arr[l:l + n1]
    R = arr[m + 1:m + 1 + n2]

    i = j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def merge_sort(arr: list[int], l: int, r: int) -> None:
    if l < r:
        m = (l + r) // 2  # find the middle point
        merge_sort(arr, l, m)  # sort first half
        merge_sort(arr, m + 1, r)  # sort second half
        merge(arr, l, m, r)  # merge the sorted halves

def read_array_from_file(filename: str) -> list[int]:
    with open(filename, 'rb') as f:
        return np.fromfile(f, dtype=np.int32).tolist()

def main():
    args = arg.parse_args()
    arr = read_array_from_file(args.file)
    if not args.quiet:
        print("Before:", arr)

    match args.algorithm:
        case "insertion":
            insertion_sort(arr)
        case "quick":
            quick_sort(arr, 0, len(arr) - 1)
        case "merge":
            merge_sort(arr, 0, len(arr) - 1)

    if not args.quiet:
        print("After:", arr)

if __name__ == "__main__":
    main()
