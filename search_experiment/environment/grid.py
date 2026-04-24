"""
Grid environment for search algorithm experiments.
"""

import json
import os
import random
from collections import deque


class Grid:
    """
    2D grid environment for experiments.

    Cell Values: 0 = open, 1 = obstacle
    Start: (0, 0), Goal: (size-1, size-1)
    Movement: 4-directional, step cost 1.0
    """

    def __init__(self, size: int, seed: int = None, obstacle_density: float = None):
        self.size = size
        self.start = (0, 0)
        self.goal = (size - 1, size - 1)

        if seed is None:
            self.seed = random.randint(0, 2**31 - 1)
            self.mode = "random"
        else:
            self.seed = seed
            self.mode = "fixed"

        self.obstacle_density = obstacle_density
        self.cells = self.generate()

    def generate(self) -> list[list[int]]:
        # Generate a valid grid with a guaranteed path from start to goal.
        # Retries up to 100 times with random states.
        random_number = random.Random(self.seed)

        density = self.obstacle_density
        if density is None:
            # Cap at 0.40 - orginally wanted to randomly select between 0.10 and 0.5,
            # but kept getting issues between 0.43 and 0.50, under this limit, it worked
            density = random_number.uniform(0.10, 0.40)

        total_cells = self.size * self.size
        # Start and goal are always open, so available obstacle slots = total - 2
        obstacle_slots = total_cells - 2
        n_obstacles = int(obstacle_slots * density)
        
        obstacle_eligible_positions = []
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) != self.start and (r, c) != self.goal:
                    obstacle_eligible_positions.append((r, c))

        for attempt in range(100):
            cells = [[0] * self.size for _ in range(self.size)]

            # Shuffle using random_number so each attempt uses a different arrangement
            random_number.shuffle(obstacle_eligible_positions)

            for position in obstacle_eligible_positions[:n_obstacles]:
                cells[position[0]][position[1]] = 1

            if self.is_connected(cells):
                # Compute density: obstacles / total cells
                actual_obstacles = sum(cells[r][c] for r in range(self.size) for c in range(self.size))
                self.obstacle_density = actual_obstacles / total_cells
                return cells

        raise RuntimeError(
            f"Could not generate a connected grid after 100 attempts "
            f"(size={self.size}, seed={self.seed}, density≈{density:.2f})"
        )

    def is_connected(self, cells: list[list[int]]) -> bool:
        # BFS from start to goal on the given cell grid to ensure goal is reachable
        frontier = deque([self.start])
        explored = {self.start}

        while frontier:
            row, col = frontier.popleft()
            if (row, col) == self.goal:
                return True
            for nr, nc in self.raw_neighbors(row, col, cells):
                if (nr, nc) not in explored:
                    explored.add((nr, nc))
                    frontier.append((nr, nc))

        return False

    def raw_neighbors(self, row: int, col: int, cells: list[list[int]]) -> list[tuple[int, int]]:
        # returns a list of the adjacent open neighbors to the passed in position
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size and cells[nr][nc] == 0:
                neighbors.append((nr, nc))
        return neighbors

    def get_neighbors(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        # public facing version of raw_neighbors
        row, col = pos
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size and self.cells[nr][nc] == 0:
                neighbors.append((nr, nc))
        return neighbors

    def is_goal(self, pos: tuple[int, int]) -> bool:
        return pos == self.goal

    def step_cost(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
        return 1.0

    def to_dict(self) -> dict:
        # convert Grid object to a dictionary
        return {
            "size": self.size,
            "seed": self.seed,
            "mode": self.mode,
            "obstacle_density": self.obstacle_density,
            "cells": self.cells,
        }

    @classmethod
    def from_dict(Grid, d: dict) -> "Grid":
        # rebuilds a grid from the dictionary without generating a new grid
        obj = object.__new__(Grid)
        obj.size = d["size"]
        obj.seed = d["seed"]
        obj.mode = d["mode"]
        obj.obstacle_density = d["obstacle_density"]
        obj.cells = d["cells"]
        obj.start = (0, 0)
        obj.goal = (obj.size - 1, obj.size - 1)
        return obj
    
    def save(self, directory: str = "grids/") -> str:
        # saves the current grid to a JSON file
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"{self.seed}.json")
        with open(path, "w") as f:
            json.dump(self.to_dict(), f)
        return path

    @classmethod
    def load(cls, seed: int, directory: str = "grids/") -> "Grid":
        # opens a saved JSON file and reconstructs the grid
        path = os.path.join(directory, f"{seed}.json")
        with open(path) as f:
            d = json.load(f)
        return cls.from_dict(d)
