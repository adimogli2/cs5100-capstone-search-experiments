"""
Heuristic functions for informed search algorithms.

All heuristics share the signature: fn(pos, goal) -> float
pos and goal are (row, col) tuples.
"""
import math

def manhattan_distance(pos: tuple[int, int], goal: tuple[int, int]) -> float:
    # sum of absolute row and column differences
    return float(abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))

def euclidean_distance(pos: tuple[int, int], goal: tuple[int, int]) -> float:
    # straight-line distance between pos and goal
    return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)

def zero_heuristic(pos: tuple[int, int], goal: tuple[int, int]) -> float:
    # always returns 0
    return 0.0

def inadmissible_heuristic(pos: tuple[int, int], goal: tuple[int, int]) -> float:
    # returns 2 times manhattan distance to create an inadmissible heuristic
    return 2.0 * manhattan_distance(pos, goal)

HEURISTICS: dict[str, callable] = {
    "manhattan": manhattan_distance,
    "euclidean": euclidean_distance,
    "zero": zero_heuristic,
    "inadmissible": inadmissible_heuristic,
}
