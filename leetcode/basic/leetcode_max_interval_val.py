"""
xn: length n. start position
yn: length n. interval length
vn: length n. value of each interval [xi, xi+yi]

select a subset of intervals such that the sum of their values is maximized.
how to compute in smaller than O(n^2) time?
"""

# def sf(xn, yn, vn):
#     n = len(xn)
#     dp = [0] * (n + 1)
#     for i in range(1, n + 1):
#         dp[i] = max(dp[i - 1], dp[i])
#         for j in range(i):
#             if xn[i - 1] >= yn[j]:
#                 dp[i] = max(dp[i], dp[j] + vn[i - 1])
#     return dp[n]


# how to compute in smaller than O(n^2) time?
def sf_non_dp(xn, yn, vn):
    n = len(xn)
    # sort by end position
    intervals = sorted(zip(xn, yn, vn), key=lambda x: x[1])
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = max(dp[i - 1], dp[i])
        for j in range(i):
            if intervals[i - 1][0] >= intervals[j][1]:
                dp[i] = max(dp[i], dp[j] + intervals[i - 1][2])
    return dp[n]

from typing import List
import bisect

def max_interval_value(x: List[int], y: List[int], v: List[int]) -> int:
    n = len(x)
    intervals = sorted(zip(x, y, v), key=lambda i: i[0] + i[1])
    
    end_points = [i[0] + i[1] for i in intervals]
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        current_start = intervals[i-1][0]
        current_value = intervals[i-1][2]
        
        j = bisect.bisect_right(end_points, current_start) - 1
        dp[i] = max(dp[i-1], dp[j] + current_value)
    
    return dp[n]

# Example usage
x = [1, 2, 3, 4, 5]
y = [2, 3, 1, 2, 1]
v = [3, 4, 2, 1, 5]

result = max_interval_value(x, y, v)
print(f"Maximum value: {result}")