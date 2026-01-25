from typing import List, Tuple

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
    
    :param prefs: Description
    :type prefs: List[List[int]]
    :param n: Description
    :type n: int
    :return: Description
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