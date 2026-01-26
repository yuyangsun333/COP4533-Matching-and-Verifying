"""
generate_out.py

Utility script for generating random matching output files (.out).
This script is intended for testing, debugging, and output-format verification only.

For Task C scalability experiments, it is recommended to generate `.out` files
using the official matcher implementation in `src/matcher.py`, since random
matchings may not be stable.
"""


import random
import sys
from typing import List, Tuple

def generate_random_matching(n: int, seed: int = None) -> list[Tuple[int, int]]:
    """
    Generate a random valid one-to-one matching.
    
    :param n: The total number of hospitals (which equals the number of students).
    :type n: int
    :param seed: Optional random seed.
    :type seed: int
    :return: A list of matched pairs (h, s), where hospital h is matched to student s.
    :rtype: list[Tuple[int, int]]
    """
    if seed is not None:
        random.seed(seed)

    # Random permutation of students 1 -> n
    students = list(range(1, n + 1))
    random.shuffle(students)

    # Pair hospital i with students[i-1]
    pairs = [(h, students[h - 1]) for h in range(1, n + 1)] # students index start from 0
    return pairs


def write_out_file(filename: str, n: int, seed: int = None) -> None:
    """
    Generate and write a random matching output file (.out).
    
    :param filename: Path to the output .out file (e.g., data/random_64.out).
    :type filename: str
    :param n: The total number of hospitals (or students).
    :type n: int
    :param seed: Optional random seed.
    :type seed: int
    """
    pairs = generate_random_matching(n, seed)

    with open(filename, "w") as f:
        for h, s in pairs:
            f.write(f"{h} {s}\n")

    print(f"Generated random matching file: {filename} (n={n})")


if __name__ == "__main__":
    """
    Usage:
        python3 scripts/generate_out.py <output_file> <n> [seed]

    Example:
        python3 scripts/generate_out.py data/random_16.out 16 42
    """
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/generate_out.py <output_file> <n> [seed]")
        sys.exit(1)

    output_file = sys.argv[1]
    n = int(sys.argv[2])

    # Seed is optional
    seed = int(sys.argv[3]) if len(sys.argv) >= 4 else None

    write_out_file(output_file, n, seed)