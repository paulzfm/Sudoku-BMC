# Generate NuSMV model for solving a Sudoku problem.

N = 9
NS = 3


def load_problem(file_name: str) -> [[int]]:
    with open(file_name, 'r') as f:
        rows = [(line.replace('\n', '').split(' '))[:N] for line in f.readlines()][:N]
        f.close()
        board = [[int(elem) for elem in col] for col in rows]
        return board


def gen_matrix(board: [[int]]) -> [[bool]]:
    def fill_in(matrix: [[bool]], i: int, j: int, k: int):
        row = (i * N + j) * N + k
        matrix[row][N * N * 0 + i * N + k] = True  # row
        matrix[row][N * N * 1 + j * N + k] = True  # col
        div1, _ = divmod(i, NS)
        div2, _ = divmod(j, NS)
        z = div1 * NS + div2
        matrix[row][N * N * 2 + z * N + k] = True  # box

    matrix = [[False for _ in range(N * N * 3)] for _ in range(N * N * N)]
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                [fill_in(matrix, i, j, k) for k in range(N)]
            else:
                fill_in(matrix, i, j, board[i][j] - 1)

    return matrix


def get_selected(board: [[int]]) -> [int]:
    selected = [0 for _ in range(N * N)]
    for i in range(N):
        for j in range(N):
            k = board[i][j] - 1 if board[i][j] > 0 else 0
            row = (i * N + j) * N + k
            selected[i * N + j] = row

    return selected


def get_modified(board: [[int]]) -> [bool]:
    modified = [True for _ in range(N * N)]
    for i in range(N):
        for j in range(N):
            if board[i][j] != 0:
                modified[i * N + j] = False

    return modified


def gen_code(matrix: [[bool]], selected: [int], modified: [bool]) -> str:
    _matrix = str([['TRUE' if elem else 'FALSE' for elem in row] for row in matrix]).replace("'", '')
    _var = ''
    _assign = ''
    for cell in range(N * N):
        if modified[cell]:
            candidates = range(cell * N, (cell + 1) * N)
            _var += 'select%i: %i..%i;\n' % (cell, cell * N, (cell + 1) * N - 1)
            _assign += 'select%i := {%s};\n' % (cell, ', '.join(map(str, candidates)))
        else:
            _var += 'select%i: %i..%i;\n' % (cell, selected[cell], selected[cell])
            # _assign += 'select%i := %i;\n' % (cell, selected[cell])

    _spec_cols = [' | '.join(['matrix[select%i][%i]' % (row, col) for row in range(N * N)])
                  for col in range(N * N * 3)]
    _spec = ' & '.join(['(%s)' % s for s in _spec_cols])

    code = """
MODULE main
DEFINE
matrix := %s;

VAR
%s

ASSIGN
%s

LTLSPEC
!G (%s);
""" % (_matrix, _var, _assign, _spec)

    return code


if __name__ == '__main__':
    prob = load_problem('sample.txt')
    source = gen_code(gen_matrix(prob), get_selected(prob), get_modified(prob))

    with open('test.smv', 'w') as f:
        f.write(source)
        f.close()
