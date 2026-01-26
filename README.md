# COP4533-Matching-and-Verifying

This repository contains the implementation for the COP4533 Programming Assignment 1 on stable matching and verification using the hospital-proposing Gale–Shapley algorithm.

## Team Members
- Name: Yuyang Sun, UFID: 38133550  
- Name: Junhao Li, UFID: 51521823

## Requirements / Dependencies
- Python **3.x**
- No external libraries are required for Task A and B.

## Project Structure
- `src/` : Core implementation files (Task A & Task B)
  - `matcher.py` : Implements the hospital-proposing Gale–Shapley algorithm (Task A).
  - `verifier.py` : Verifies whether a proposed matching is valid and stable (Task B).

- `data/` : Example input/output files for quick testing
  - `example.in` : Sample preference input file.
  - `example.out` : Sample matching output file.

- `scripts/` : Helper scripts for testing / debugging / scalability experiments
  - `generate_in.py` : Generates random `.in` preference files of size `n`.
  - `generate_out.py` : Generates random valid `.out` matchings (debug/format testing only; may be unstable).

- `README.md` : Project documentation and usage instructions.

## Input Format

### Matcher

Input describes preferences for a one-to-one market with complete strict rankings.
1. First line: integer `n`
2. Next `n` lines: hospital preference lists (each line is a permutation of `1..n`)
3. Next `n` lines: student preference lists (each line is a permutation of `1..n`)

### Verifier

The virifier takes **two input files**:
- **Preference file (`.in`)**: the same format as the matcher input, containing the hospital and student rankings.
- **Matching file (`.out`)**: the proposed matching to be verified.

The `.out` file must contain exactly `n` lines, each in the format:

```text
h s
```
Meaning hospital `h` is matched to student `s`.

## Output Format 

### Matcher

The matcher prints **n lines**, one per hospital `i`:

```text
i j
```    
meaning hospital `i` is matched to student `j`.

### Verifier

The verifier prints a single status message if the matching is both valid and stable:

```text
VALID STABLE
```

Otherwise, it prints one of the following depending on whether the matching is invalid or contains a blocking pair:

```text
INVALID: ...
UNSTABLE: Blocking pair (h, s)
```

## Task A: Matcher

### How to Run
Example Input file: data/example.in

From the repository root, run:

```bash
python3 src/matcher.py data/example.in
```
Output: prints n lines in the format i j (one line per hospital).

## Task B: Verifier

### How to Run
Example Input file: data/example.in
Example Matching Output file: data/example.out

From the repository root, run:

```bash
python3 src/verifier.py data/example.in data/example.out
```
Output: prints one of the following messages:
- `VALID STABLE` (matching is valid and stable)
- `INVALID: ...` (matching is not a valid one-to-one assignment)
- `UNSTABLE: Blocking pair (h, s)` (matching contains a blocking pair)
