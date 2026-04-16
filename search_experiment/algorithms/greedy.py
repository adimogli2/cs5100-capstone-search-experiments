"""
Greedy Best-First Search
========================
Greedy Best-First Search expands the node that appears closest to the
goal according to the heuristic h(n), completely ignoring path cost g(n).

Data structure : Min-heap priority queue ordered by h(n) alone (heapq)
Completeness   : NOT complete in general — can get trapped in loops
                 (with cycle detection it is complete on finite graphs).
Optimality     : NOT optimal — because g(n) is ignored, the first path
                 found may not be the cheapest.
Time complexity : O(b^m) in the worst case (heuristic-dependent).
Space complexity: O(b^m) — keeps all generated nodes in memory.

Relationship to A*: Greedy is A* with the g(n) term removed.
                    It is faster in practice but sacrifices optimality.
"""

import heapq

from algorithms.base import SearchAlgorithm, SearchResult
from heuristics.heuristics import manhattan_distance


class GreedyBestFirst(SearchAlgorithm):
    """Greedy Best-First Search — informed, not optimal, heuristic-driven."""

    def __init__(self, grid, heuristic=None):
        """
        Parameters
        ----------
        grid      : Grid
        heuristic : callable(pos, goal) -> float
                    Defaults to manhattan_distance if not provided.
        """
        if heuristic is None:
            heuristic = manhattan_distance
        super().__init__(grid, heuristic)

    def search(self) -> SearchResult:
        """
        Implementation guide (fill this in when ready):

        1. Initialise a min-heap frontier.
           Push (h(start), counter, start) where
             h(start) = self.heuristic(start, self.grid.goal).

        2. Initialise an explored set (empty at start).

        3. Initialise a came_from dict: {start: None}.

        4. Pop the lowest-h entry with heapq.heappop.
           Skip if already in explored; then mark explored.
           Increment nodes_expanded.

        5. If the popped node is the goal:
           - Call self.reconstruct_path(came_from, goal).
           - Compute path_cost as (len(path) - 1) * 1.0.
           - Return SearchResult(path, path_cost, nodes_expanded, success=True).

        6. For each neighbor from self.grid.get_neighbors(pos):
           - Skip if already in explored.
           - Record came_from[neighbor] = pos  (only if not yet set).
           - Compute h = self.heuristic(neighbor, self.grid.goal).
           - Push (h, counter, neighbor) onto the heap.

        7. If the heap empties without finding the goal,
           return self.no_path_result().
        """
        start = self.grid.start
        goal  = self.grid.goal

        counter  = 0
        explored = set()
        came_from = {start: None}
        frontier  = [(self.heuristic(start, goal), counter, start)]
        nodes_expanded = 0

        while frontier:
            _, _, pos = heapq.heappop(frontier)

            if pos in explored:
                continue
            explored.add(pos)
            nodes_expanded += 1

            if pos == goal:
                path = self.reconstruct_path(came_from, pos)
                return SearchResult(
                    path=path,
                    path_cost=float(len(path) - 1),
                    nodes_expanded=nodes_expanded,
                    success=True,
                )

            for neighbor in self.grid.get_neighbors(pos):
                if neighbor not in explored:
                    if neighbor not in came_from:
                        came_from[neighbor] = pos
                    h = self.heuristic(neighbor, goal)
                    counter += 1
                    heapq.heappush(frontier, (h, counter, neighbor))

        return self.no_path_result()
