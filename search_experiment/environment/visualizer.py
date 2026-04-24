"""
Visualiser for Grid instances.

Characters:
  S  start cell (0, 0)
  G  goal cell (n-1, n-1)
  #  obstacle
  *  path cell (when a path is supplied)
  .  open cell
"""

from environment.grid import Grid

def visualize(grid: Grid, path: list[tuple[int, int]] | None = None) -> None:
    # prints a visual representation of a grid
    if path:
        path_set = set(path)
    else:
        path_set = set()

    for r in range(grid.size):
        row_chars = []
        for c in range(grid.size):
            pos = (r, c)
            if pos == grid.start:
                row_chars.append("S")
            elif pos == grid.goal:
                row_chars.append("G")
            elif grid.cells[r][c] == 1:
                row_chars.append("#")
            elif pos in path_set:
                row_chars.append("*")
            else:
                row_chars.append(".")
        print(" ".join(row_chars))
