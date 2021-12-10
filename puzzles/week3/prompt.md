# Summary

This week's puzzle is filtering.

Given a list of numbers, return the biggest number meeting some criteria.

# Input

An integer, f
0 <= f <= 5

f space seperated integers, y[i], 0 <= i < f
1 <= y[i] <= 100

An integer, n
0 <= n <= 100

n space seperated integers, x[i], 0 <= i < n
1 <= x[i] <= 2147483647

Input will be provided on the stdin stream on 4 lines.

# Output

A single integer, the biggest number in x that is a multiple of every number in y.

If no such number exists, output -1.

Output should be provided on the stdout stream, with a single integer on each line.

# Example

## Input:

3
3, 5, 3
7
40, 81, 15, 25, 30, 9, 3

## Output:

30
