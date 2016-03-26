# Sudoku-BMC

Using NuSMV bounded model checker to solve sudoku.

### Prerequisite

NuSMV 2.5 or higher version should be pre-installed.

Make sure that `NuSMV` command is in your system PATH.

### Usage

#### The naive solver (faster)

	python3 sudoku_naive.py <input_file> [-on | -off]

Options `-on | -off` mean whether to apply optimising strategy on NuSMV model construction.

#### The 0-1 cover solver (slower)

	python3 sudoku_01.py <input_file>

Notice that the input file should be in format like:

```
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```

where 0 denotes the blanks need to be filled in. See `testcases/` for more examples.

### Theory

See [report](https://github.com/paulzfm/Sudoku-BMC/blob/master/doc/report.pdf) for details.
