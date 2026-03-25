import numpy as np
import numpy.typing as npt
import argparse

DATA: str = "data/"

args = argparse.ArgumentParser(description="Generate random arrays for sorting algorithms.")
args.add_argument("size", type=int, help="Size of the array to generate.")

def generate_random_signed_array(size: int) -> npt.NDArray[np.int32]:
    return np.random.randint(-2**31, 2**31, size=size, dtype=np.int32)

def save_array_to_file(arr: npt.NDArray[np.int32], filename: str) -> None:
    arr.tofile(filename)


if __name__ == "__main__":
    args = args.parse_args()
    random_array = generate_random_signed_array(args.size)
    save_array_to_file(random_array, f"{DATA}random_array_{args.size}.bin")
    print(f"Generated random array of size {args.size} and saved to {DATA}random_array_{args.size}.bin")
