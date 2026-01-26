import random
import sys
from typing import List

def generate_preferences(n: int) -> List[List[int]]:
    """
    Generate random strict preference lists.
    
    :param n: The total number of hospitals (or students).
    :type n: int
    :return: A list of n preference lists.
    :rtype: List[List[int]]
    """
    prefs = []
    base = list(range(1, n + 1))

    for _ in range(n):
        perm = base[:] # copy
        random.shuffle(perm) # random permutation
        prefs.append(perm)
    
    return prefs

def write_in_file(filename: str, n: int, seed: int = None) -> None:
    """
    Generate and write a random stable-matching input file (.in).

    :param filename: Path to the output input file (e.g., data/random_64.in).
    :type filename: str
    :param n: The total number of hospitals (or students).
    :type n: int
    :param seed: Optional random seed.
    :type seed: int
    """
    if seed is not None:
        random.seed(seed)

    hospital_prefs = generate_preferences(n)
    student_prefs = generate_preferences(n)

    with open(filename, 'w') as f:
        f.write(f"{n}\n")

        for row in hospital_prefs:
            f.write(" ".join(map(str, row)) + "\n")

        for row in student_prefs:
            f.write(" ".join(map(str, row)) + "\n")
        
    print(f"Generated input file: {filename} (n={n})")


if __name__ == "__main__":
    """
    Usage:
        python3 scripts/generate_in.py <output_file> <n> [seed]

    Example:
        python3 scripts/generate_in.py data/random_16.in 16 42
    """
    
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/generate_in.py <output_file> <n> [seed]")
        sys.exit(1)

    output_file = sys.argv[1]
    n = int(sys.argv[2])

    # Seed is optional
    seed = int(sys.argv[3]) if len(sys.argv) >= 4 else None
    
    write_in_file(output_file, n, seed)