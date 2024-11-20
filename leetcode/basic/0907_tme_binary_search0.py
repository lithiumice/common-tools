
from typing import List

def binary_search(arr: List, target: int):
    """
    Args:
        arr: List
        target: int
    Return: Bool
    """
    arr.sort()
    left = 0
    right = len(arr) - 1
    while left<=right:
        mid = (left + right)//2
        
        if arr[mid] == target:
            return True
        elif arr[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
            
    return False
            

examples = [
    [[0, 1, 5, 7, 9, 13], 5],
    [[0, 1, 5, 5, 5, 7, 9, 13], 5],
    [[0, 1, 5, 7, 9, 13], 6],
    [[0, 1, 5, 7, 9, 13, 4, 1], 5],
]

for example in examples:
    arr, target = example
    ret = binary_search(arr, target=target)
    print(f"{arr=} {target=}, Return: {ret}")
    
    
