"""
Base classes and result type for all search algorithms.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class SearchResult:
    # outputs for a search run
    path: list # ordered list of (row, col) tuples from start to goal
    path_cost: float # total cost of the path (sum of step costs)
    nodes_expanded: int # number of nodes popped from the frontier during search
    success: bool # True if the goal was reached

class SearchAlgorithm(ABC):
    # abstract base class fo search algorithms
    # subclasses implement search(), but can use the helper methods

    def __init__(self, grid, heuristic=None):
        # informed algorithms pass heuristic, uninformed leave it as None
        self.grid = grid
        self.heuristic = heuristic

    @abstractmethod
    def search(self) -> SearchResult:
        """Run the search and return a SearchResult."""

    def reconstruct_path(self, came_from: dict[tuple, tuple], current: tuple) -> list[tuple]:
        # walk came_from dictionary backwards from current node to start node, returning path in start to goal order
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path

    def no_path_result(self) -> SearchResult:
        # return for failed searches, not necessary, but good for consistency
        return SearchResult(path=[], path_cost=0.0, nodes_expanded=0, success=False)
