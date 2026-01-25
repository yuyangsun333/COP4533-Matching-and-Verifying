# COP4533-Matching-and-Verifying

This repository contains the implementation for the COP4533 Programming Assignment 1 on stable matching and verification using the hospital-proposing Gale–Shapley algorithm.

## Team Members
- Name: Yuyang Sun, UFID: 38133550  
- Name: Junhao Li, UFID: 51521823

## Requirements / Dependencies
- Python **3.x**
- No external libraries are required for Task A.

## Input Format
Input describes preferences for a one-to-one market with complete strict rankings.
1. First line: integer `n`
2. Next `n` lines: hospital preference lists (each line is a permutation of `1..n`)
3. Next `n` lines: student preference lists (each line is a permutation of `1..n`)

## Output Format 

### Matcher

The matcher prints **n lines**, one per hospital `i`:

```text
i j
```    
meaning hospital `i` is matched to student `j`.


## Task A: Matcher

### How to Run
Example Input file: data/example.in

From the repository root, run:

```bash
python3 src/matcher.py data/example.in
```
Output: prints n lines in the format i j (one line per hospital).