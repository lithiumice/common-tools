# 题目概述：
# 1. 给定一个长度为N的整数数组a[]。
# 可以进行任意次操作：选择相邻的两个数，将它们的符号都翻转。
# 3. 符号翻转意味着将正数变为负数，负数变为正数（即num = -num）。
# 目标是通过这些操作后得到数组的最大和。
# 输入：
# 第一行：一个整数N，表示数组长度（1 ≤ N ≤ 30000）
# 第二行：N个整数，表示数组a[1], a[2], ..., a[N]（-1000000000 ≤ a[i] ≤ 1000000000）
# 输出：
# 一个整数，表示经过任意次操作后数组的最大和。


# 用dfs找出能否通过翻转把所有负数变成正数。如果不能最后会只剩下一个负号，最后把这个负号弄到最小数；如果可以全部翻转答案就是全部数的绝对值之和



# def max_array_sum(arr):
#     n = len(arr)
#     abs_sum = sum(abs(x) for x in arr)
    
#     def dfs(index, flip):
#         if index == n:
#             return flip % 2 == 0
        
#         if arr[index] < 0:
#             return dfs(index + 1, flip + 1)
#         else:
#             return dfs(index + 1, flip) or dfs(index + 1, flip + 1)
    
#     if dfs(0, 0):
#         return abs_sum
#     else:
#         return abs_sum - 2 * min(abs(x) for x in arr)


def max_array_sum(arr):
    n = len(arr)
    sum = 0
    for i in range(n-1):
        if arr[i] * arr[i+1] < 0:
            sum += abs(arr[i]) + abs(arr[i+1])
            arr[i] *= -1
            arr[i+1] *= -1
             
    return sum + arr[n-1]
             


# 读取输入
# n = int(input())
# arr = list(map(int, input().split()))
n = 5
# arr = [1,-2,3,-4,5]
arr = [2,-15,-1,-8,16]

# 计算并输出结果
print(max_array_sum(arr))