from typing import List, Tuple
from matcher import data_reader
import sys

def verify_validity(n: int, pairs: List[Tuple[int, int]]) -> Tuple[bool, str]:
    """
    Verify whether a proposed matching is a valid one-to-one assignment.
    
    :param n: The total number of hospitals (which equals the number of students).
    :type n: int
    :param pairs: A list of matched pairs where each tuple is (hospital_id, student_id).
    :type pairs: List[Tuple[int, int]]
    :return: A tuple containing a boolean (True if valid) and a status message.
    :rtype: Tuple[bool, str]
    """
    if n <= 0:
        return False, "INVALID: n must be >= 1"

    # A perfect one-to-one matching must have exactly n pairs
    if len(pairs) != n:
        return False, f"INVALID: expected {n} pairs, got {len(pairs)}"
    
    # Seen array: False means not seen yet
    seen_hospitals = [False] * (n + 1) # IDs start from 1
    seen_students = [False] * (n + 1)

    for(h, s) in pairs:
        # Range check
        if not (1 <= h <= n):
            return False, f"INVALID: hospital {h} out of range <1 - {n}>"
        if not (1 <= s <= n):
            return False, f"INVALID: student {s} out of range <1 - {n}>"

        # Duplicate check
        if seen_hospitals[h]:
            return False, f"INVALID: hospital {h} appears more than once"
        if seen_students[s]:
            return False, f"INVALID: student {s} matched more than once"

        # Mark as seen
        seen_hospitals[h] = True
        seen_students[s] = True

    # If we reach here, the matching is complete and one-to-one
    return True, "VALID"


def get_match(n: int, pairs: List[Tuple[int, int]]) -> Tuple[List[int], List[int]]:
    """
    Build two lookup tables for the matching (both directions).
    
    :param n: The total number of hospitals (which equals the number of students).
    :type n: int
    :param pairs: A list of matched pairs where each tuple is (hospital_id, student_id).
    :type pairs: List[Tuple[int, int]]
    :return: Two matching maps:

        - match_h: a list where match_h[h] gives the student matched to hospital h.
        - match_s: a list where match_s[s] gives the hospital mateched to student s.
    :rtype: Tuple[List[int], List[int]]
    """
    # Initialize with 0 (unused), index from 1->n
    match_h = [0] * (n + 1)
    match_s = [0] * (n + 1)

    for (h, s) in pairs:
        # Store both directions
        match_h[h] = s
        match_s[s] = h
    
    return match_h, match_s


def get_rank(prefs: List[List[int]], n: int) -> List[List[int]]:
    """
    Convert ordered preference lists into a rank lookup table.
    
    :param prefs: Preference lists from the input file.
    :type prefs: List[List[int]]
    :param n: The total number of hospitals (which equals the number of students).
    :type n: int
    :return: A 2D rank table where rank[x][y] gives how agent x ranks partner y.
             Lower values mean higher preference (0 = best).
    :rtype: List[List[int]]
    """
    # Create (n+1) x (n+1) table, index 0 is unused
    rank = [[0] * (n + 1) for _ in range(n + 1)] # rank[n + 1][n + 1]

    # x is the agent id (hospital or student)
    for x in range(1, n + 1):
        # index is the rank position in x's preference list (0 = best)
        for index in range(n):
            y = prefs[x - 1][index] # prefs is 0-indexed, so agent x's row is prefs[x-1]
            rank[x][y] = index # y is the 'index'-th choice of agent x
    
    return rank

def verify_preferences(n: int,
                       hospital_prefs: List[List[int]],
                       student_prefs: List[List[int]]) -> Tuple[bool, str]:
    """
    Verify input preference tables are well-formed:
    
    :param n: The total number of hospitals (which equals the number of students)
    :type n: int
    :param hospital_prefs: Preference lists of hospitals.
    :type hospital_prefs: List[List[int]]
    :param student_prefs: Preference lists of students.
    :type student_prefs: List[List[int]]
    :return: Return [True, VALID_INPUT], if the input preference tables are well-formed.
    :rtype: Tuple[bool, str]
    """
    if n <= 0:
        return False, "INVALID: n must be >= 1"

    if len(hospital_prefs) != n:
        return False, f"INVALID: expected {n} hospital preference lines, got {len(hospital_prefs)}"
    if len(student_prefs) != n:
        return False, f"INVALID: expected {n} student preference lines, got {len(student_prefs)}"

    return True, "VALID_INPUT"


def verify_stability(n: int,
                     hospital_prefs: List[List[int]],
                     student_prefs: List[List[int]],
                     pairs: List[Tuple[int, int]]) -> Tuple[bool, str]:
    """
    Verify whether a given matching is stable.
    
    :param n: The total number of hospitals (which equals the number of students).
    :type n: int
    :param hospital_prefs: Hospital preference lists read from the input file.
    :type hospital_prefs: List[List[int]]
    :param student_prefs: Student preference lists read from the input file.
    :type student_prefs: List[List[int]]
    :param pairs: matching output, list of (h, s)
    :type pairs: List[Tuple[int, int]]
    :return: (True, "STABLE") if no blocking pair exists,
             otherwise (False, "UNSTABLE: blocking pair (h, s)").
    :rtype: Tuple[bool, str]
    """
    # Build matching maps
    match_h, match_s = get_match(n, pairs)

    # Build rank lookup tables
    hospital_rank = get_rank(hospital_prefs, n) # hospital_rank[h][s]
    student_rank = get_rank(student_prefs, n) #student_rank[s][h]

    # For each hospital h, only consider students it prefers over its current match.
    for h in range(1, n + 1):
        current_s = match_h[h]

        # Iterate hospital h's preference list untile reaching current_s.
        for s in hospital_prefs[h - 1]: # h - 1 represent current hospital
            if s == current_s:
                break
            
            current_h = match_s[s] # current_h: student's currently matched hospital
            # student s prefers h over its current hospital.
            if student_rank[s][h] < student_rank[s][current_h]:
                return False, f"UNSTABLE: Blocking pair ({h}, {s})"
            
    return True, "STABLE"


def read_matching(out_path: str) -> List[Tuple[int, int]]:
    """
    Read the matching output file (.out).
    Each line should be: hospital_id student_id
    
    :param out_path: Output file path (as one of the input in verifier).
    :type out_path: str
    :return: A list of matched pairs where each tuple is (hospital_id, student_id).
    :rtype: List[Tuple[int, int]]
    """
    pairs = []

    with open(out_path, "r", encoding="utf-16") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            h, s = map(int, line.split())
            pairs.append((h, s))

    return pairs

def main():
    """
    Run verifier from command line:

        Usage: python3 src/verifier.py <input_file> <output_file>
    """
    if len(sys.argv) != 3:
        print("Usage: python3 src/verifier.py <input_file> <output_file>")
        sys.exit(2)
    
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    # Read input preferences
    try:
        n, hospital_prefs, student_prefs = data_reader(in_file)
    except FileNotFoundError:
        print(f"INVALID: input file not found: {in_file}")
        return False
    except Exception as e:
        print(f"INVALID: failed to parse input file: {e}")
        return False
    
    # Validate preference tables
    valid_in, inmsg = verify_preferences(n, hospital_prefs, student_prefs)
    if not valid_in:
        print(inmsg)
        return False

    # Read matching output pairs
    pairs = read_matching(out_file)

    # Validity check first (Task b(a))
    is_valid, vmsg = verify_validity(n, pairs)
    if not is_valid:
        print(vmsg)
        return False

    # Stability check (Task b(b))
    is_stable, smsg = verify_stability(n, hospital_prefs, student_prefs, pairs)
    if not is_stable:
        print(smsg)
    else:
        print("VALID STABLE")


if __name__ == "__main__":
    main()