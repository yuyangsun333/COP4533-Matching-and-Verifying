from typing import List, Tuple

def verify_validity(n: int, pairs: List[Tuple[int, int]]) -> Tuple[bool, str]:
    """
    Docstring for verify_validity
    
    :param n: The total number of hospitals (which equals the number of students).
    :type n: int
    :param pairs: A list of matched pairs where each tuple is (hospital_id, student_id).
    :type pairs: List[Tuple[int, int]]
    :return: A tuple containing a boolean (True if valid) and a status message.
    :rtype: Tuple[bool, str]
    """
    if n <= 0:
        return False, "INVALID: n must be >= 1"

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

    return True, "VALID"

def get_match(n: int, paris: List[Tuple[int, int]]) -> Tuple[List[int], List[int]]:
    """
    Docstring for get_match
    
    :param n: The total number of hospitals (which equals the number of students).
    :type n: int
    :param paris: A list of matched pairs where each tuple is (hospital_id, student_id).
    :type paris: List[Tuple[int, int]]
    :return: Two matching maps:

        - match_h: a list where match_h[h] gives the student matched to hospital h.
        - match_s: a list where match_s[s] gives the hospital mateched to student s.
    :rtype: Tuple[List[int], List[int]]
    """
    match_h = [0] * (n + 1)
    match_s = [0] * (n + 1)

    for (h, s) in paris:
        match_h[h] = s
        match_s[s] = h
    
    return match_h, match_s
