from collections import deque
import sys

def data_reader(file_path):
    """
    Read the input data and return as 
        n: number of hospitals/students
        hostial preferences list
        student preferences list
    """
    try: # read file
        with open(file_path, 'r') as file:
            data = file.readlines()
    except FileNotFoundError:
        raise ValueError(f"INVALID: file not found: {file_path}")
    
    # Remove any trailing newlines and spaces
    data = [line.strip() for line in data if line.strip()]

    if not data:
        raise ValueError("INVALID: input file is empty or improperly formatted.")

    # parse n
    try:
        n = int(data[0])
    except ValueError:
        raise ValueError("INVALID: first line must be an integer")

    if n < 1:
        raise ValueError("INVALID: n must be >= 1.")
    
    expected_lines = 1 + 2*n
    if len(data) != expected_lines:
        raise ValueError(
            f"INVALID: expected {expected_lines} lines (1 + 2n), got {len(data)}."
        )

    n = int(data[0])
    hospital_prefs = []
    student_prefs = []

    for i in range(1, n + 1):
        prefs = list(map(int, data[i].split()))
        hospital_prefs.append(prefs)

    for i in range(n + 1, 2 * n + 1):
        prefs = list(map(int, data[i].split()))
        student_prefs.append(prefs)

    return n, hospital_prefs, student_prefs

# print(data_reader('data/example.in'))

def gale_shapley(n, hospital_prefs, student_prefs):
    """ 
    Implement the Gale-Shapley algorithm to find a stable matching
    """
    hospital_free = deque()

    for i in range(0, n):
        hospital_free.append(i + 1)

    # Init all hospitals and students as free
    hospital_match = [-1] * (n + 1)
    student_match = [-1] * (n + 1)
    hospital_next = [0] * (n + 1)  # Track next student to propose to for each hospital

    # position of hospital in student's preference list
    rank = [[0] * (n + 1) for _ in range(n + 1)]

    for s in range(1, n + 1):
        for pos in range(n): # 0 is best
            h = student_prefs[s - 1][pos]
            rank[s][h] = pos

    while hospital_free:
        current = hospital_free.popleft()
        current_index = current - 1

        if hospital_next[current] >= n:
            continue

        next_i = hospital_next[current]
        student = hospital_prefs[current_index][next_i]
        hospital_next[current] += 1

        if student_match[student] == -1: # student is not matched
            hospital_match[current] = student
            student_match[student] = current
        else:
            current_match = student_match[student]
            
            # check student preference
            if rank[student][current] < rank[student][current_match]:
                hospital_match[current] = student
                student_match[student] = current
                hospital_match[current_match] = -1
                hospital_free.append(current_match)
            else:
                hospital_free.append(current)

    return hospital_match[1:]

# Test:
# n, hospital_prefs, student_prefs = data_reader('data/example.in')
# matching = gale_shapley(n, hospital_prefs, student_prefs)
# print("Hospital Matches:", matching)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 src/matcher.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    n, hospital_prefs, student_prefs = data_reader(input_file)
    matching = gale_shapley(n, hospital_prefs, student_prefs)
    #print("n =", n)


    for i, student in enumerate(matching, start=1):
        print(i, student)


if __name__ == "__main__":
    main()