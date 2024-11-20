
from pprint import pprint

from typing import Optional


def solve_island_num(matrix):
    row = len(matrix)
    col = len(matrix[0])

    visited = [[0] * col] * row
    
    dirs = [
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0],
    ]
    
    def bfs(x, y):
        stack = [[x, y]]
        while stack:
            pprint(f"{stack=}")
            pprint(f"{visited=}")
            i, j = stack.pop()
            visited[i][j] = 1
            for dir in dirs:
                nx, ny = i + dir[0], j + dir[1]
                if (nx<0 or ny<0 or nx>=row or ny>=col):
                    continue
                if visited[nx][ny] or not matrix[nx][ny]:
                    continue
                stack.append([nx, ny])
                visited[nx][ny] = 1
            
    island_num = 0
    
    for i in range(row):
        for j in range(col):
            if not visited[i][j] and matrix[i][j]:
                island_num += 1
                visited[i][j] = 1
                bfs(i, j)

    return island_num


if __name__ == "__main__":
    # correct answer = 3
    exmaple = [
        [1, 0, 0, 1,],
        [0, 1, 0, 1,],
        [1, 1, 0, 1,],
        [1, 0, 0, 1,],
    ]
    
    ret = solve_island_num(matrix=exmaple)
    print(f"Return: {ret}")
