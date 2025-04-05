#include <vector>
#include <queue>
#include <set>
#include <tuple>
#include <cstdio>

using namespace std;

void flip(vector<vector<int>>& matrix, int x, int y) {
    int n = matrix.size();
    int m = matrix[0].size();
    vector<pair<int, int>> directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
    matrix[x][y] ^= 1;
    for (auto [dx, dy] : directions) {
        int nx = x + dx;
        int ny = y + dy;

        if (0 <= nx && nx < n && 0 <= ny && ny < m) {
            matrix[nx][ny] ^= 1; // Flip the neighboring cells
        }
    }
}

bool is_all_zero(const vector<vector<int>>& matrix) {
    for (const auto& row : matrix) {
        for (int cell : row) {
            if (cell != 0) {
                return false;
            }
        }
    }
    return true;
}

bool min_flips_to_zero(vector<vector<int>> matrix) {
    int n = matrix.size();
    int m = matrix[0].size();
    using MatrixState = vector<vector<int>>;

    queue<MatrixState> q;
    set<MatrixState> visited;

    q.push(matrix);
    visited.insert(matrix);

    while (!q.empty()) {
        auto state = q.front();
        q.pop();

        if (is_all_zero(state)) {
            return true;
        }

        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                MatrixState new_state = state; // create a copy of the current state
                flip(new_state, i, j);
                if (visited.find(new_state) == visited.end()) {
                    visited.insert(new_state);
                    q.push({new_state});
                }
            }
        }
    }

    return 0;
}

int main() {
    vector<vector<int>> matrix = {
            {1, 0, 1},
            {0, 1, 0},
            {1, 0, 1}
    };

    int result = min_flips_to_zero(matrix);
    printf("ok : %d\n", result);

    return 0;
}
