# Using NuSMV to solve a Sudoku problem.

N = 9
NS = 3
opt = False


def load_problem(file_name: str) -> [[int]]:
    with open(file_name, 'r') as f:
        rows = [(line.replace('\n', '').split(' '))[:N] for line in f.readlines()][:N]
        f.close()
        board = [[int(elem) for elem in col] for col in rows]
        return board


def get_conflicts(idx) -> [int]:
    row, col = divmod(idx, N)
    row_conflicts = set(range(row * N, (row + 1) * N))
    col_conflicts = set(range(col, N * N, N))
    box_row, _ = divmod(row, NS)
    box_col, _ = divmod(col, NS)
    start = box_row * NS * N + box_col * NS
    box_conflicts = []
    for dx in range(NS):
        for dy in range(NS):
            box_conflicts.append(start + dx * N + dy)
    box_conflicts = set(box_conflicts)
    conflicts = list((row_conflicts.union(col_conflicts)).union(box_conflicts))
    conflicts.remove(idx)

    return conflicts


def gen_candidates(board: [[int]]) -> [[int]]:
    candidates = [set() for _ in range(N * N)]
    repeat = False
    for i in range(N):
        for j in range(N):
            idx = i * N + j
            if board[i][j] == 0:
                if opt:
                    conflicts = set([board[to_row(con)][to_col(con)] for con in get_conflicts(idx)])
                    numbers = set(range(1, N + 1))
                    c = numbers - conflicts
                    if len(c) == 1:
                        board[i][j] = (list(c))[0]
                        repeat = True
                    candidates[idx] = c
                else:
                    candidates[idx] = range(1, N + 1)
            else:
                candidates[idx] = [board[i][j]]

    if opt and repeat:
        return gen_candidates(board)
    return candidates


def to_row(idx: int) -> int:
    ret, _ = divmod(idx, N)
    return ret


def to_col(idx: int) -> int:
    _, ret = divmod(idx, N)
    return ret


def gen_spec(board: [[int]]) -> str:
    all_specs = []
    for idx in range(N * N):
        row, col = divmod(idx, N)
        all_specs.extend(['board[%i] != board[%i]' % (idx, other)
                          for other in get_conflicts(idx) if other > idx])

    return ' & '.join(all_specs)


def print_board(board: [[int or str]]):
    for i in range(N):
        print(' '.join(map(str, board[i])))


code = """-- auto generated model
MODULE main
VAR
board: array 0..80 of 1..9;

ASSIGN
%s

LTLSPEC
!G (%s);
"""


def gen_code(candidates: [[int]], spec: str) -> str:
    assigns = ['board[%i] := {%s};' % (idx, ', '.join(map(str, candidates[idx]))) for idx in range(N * N)]
    return code % ('\n'.join(assigns), spec)


if __name__ == '__main__':
    import sys

    if len(sys.argv) >= 2:
        if len(sys.argv) >= 3:
            opt = True if sys.argv[2] == '-on' else False
        input_file = sys.argv[1]
    else:
        print('Usage: python %s <input_file> [-on | -off]')
        sys.exit(1)

    prob = load_problem(input_file)
    # show problem
    print('-> problem <-')
    print_board(prob)

    # construct model
    src = gen_code(gen_candidates(prob), gen_spec(prob))
    with open('tmp.smv', 'w') as f:
        f.write(src)
        f.close()

    # call NuSMV
    import os

    print('running NuSMV...')
    os.system('NuSMV -bmc tmp.smv > tmp.out')
    print('done')

    # read output
    with open('tmp.out', 'r') as f:
        content = f.read()
        f.close()

    # parse output
    import re

    pat = re.compile(r'board\[(?P<index>\d+)\] = (?P<val>[1-9])')
    answer = [[0 for _ in range(N)] for _ in range(N)]

    for match in pat.finditer(content):
        idx = int(match.group('index'))
        answer[to_row(idx)][to_col(idx)] = match.group('val')

    # display answer
    print('-> answer <-')
    print_board(answer)
