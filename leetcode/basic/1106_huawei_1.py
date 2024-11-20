"""
给定一个n*n的二维数组，只有0,1，
二维数组中若水平或者垂直方向有相同的数字则视为连通的，
替换二维驻足中所有与边界不联通的0.
"""

def replace_zero(input_mat):
    n = len(input_mat)
    visited = [[False]*n for _ in range(n)]
    
    print(f"input_mat: {input_mat}")
    
    def bfs(i, j):
        queue = [(i, j)]
        visited[i][j] = True
        while queue:
            i, j = queue.pop(0)
            for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                if 0 <= x < n and 0 <= y < n and input_mat[x][y] == 0 and not visited[x][y]:
                    queue.append((x, y))
                    visited[x][y] = True
    
    print(f"visited: {visited}")
    # 找出所有不与边界联通的0的
    for i in range(n):
        for j in range(n):
            if input_mat[i][j] == 0 and not visited[i][j]:
                bfs(i, j)
                
    # 将其他不与边界联通的0替换为1
    return input_mat


if __name__ == "__main__":
    input_mat = [
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 1, 1]
    ]
    
    correct_ans = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 0, 1, 1]
    ]
    output_mat = replace_zero(input_mat)
    print(output_mat)    
    