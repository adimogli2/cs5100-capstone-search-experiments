"""
A* Search
=========
A* combines the actual cost from the start g(n) with a heuristic
estimate of remaining cost h(n) to guide search via f(n) = g(n) + h(n).

Data structure : Min-heap priority queue ordered by f(n) = g(n) + h(n) (heapq)
Completeness   : Complete — finds a solution if one exists (finite graphs,
                 non-negative costs).
Optimality     : Optimal when the heuristic is ADMISSIBLE (never overestimates).
                 With a CONSISTENT heuristic, A* is also optimally efficient —
                 it expands no node more than once.
Time complexity : O(b^d) in the worst case; much better in practice with a
                 good heuristic.  With a perfect heuristic: O(d).
Space complexity: O(b^d) — all generated nodes must be kept in memory.

Admissibility requirement:
  h(n) <= true cost to goal for all n.
  manhattan_distance and euclidean_distance are both admissible on a
  4-directional grid with uniform cost 1.0.
  zero_heuristic is trivially admissible (degenerates to UCS).
  inadmissible_heuristic (2 * manhattan) is NOT admissible and may
  return suboptimal paths — included deliberately to test the effect.

Consistency (stronger than admissibility):
  h(n) <= step_cost(n, n') + h(n') for every successor n'.
  Guarantees A* expands each node at most once.
"""

import heapq

from algorithms.base import SearchAlgorithm, SearchResult
from heuristics.heuristics import manhattan_distance


class AStar(SearchAlgorithm):
    """A* Search — informed, complete, optimal with admissible heuristic."""

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
        start = self.grid.start
        goal  = self.grid.goal

        # g_score[pos] = cheapest known cost from start to pos
        g_score: dict[tuple, float] = {start: 0.0}

        # came_from[pos] = the node that preceded pos on the cheapest path
        came_from: dict[tuple, tuple | None] = {start: None}

        # Min-heap entries: (f, tie-break counter, g, pos)
        # The counter prevents tuple comparison falling through to pos tuples
        # if two entries share the same f value.
        counter  = 0
        h_start  = self.heuristic(start, goal)
        frontier = [(h_start, counter, 0.0, start)]

        nodes_expanded = 0

        while frontier:
            f, _, g, pos = heapq.heappop(frontier)

            # Stale entry: a cheaper path to pos was already processed
            if g > g_score[pos]:
                continue

            nodes_expanded += 1

            if pos == goal:
                path = self.reconstruct_path(came_from, pos)
                return SearchResult(
                    path=path,
                    path_cost=g_score[goal],
                    nodes_expanded=nodes_expanded,
                    success=True,
                )

            for neighbor in self.grid.get_neighbors(pos):
                tentative_g = g_score[pos] + self.grid.step_cost(pos, neighbor)

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor]   = tentative_g
                    came_from[neighbor] = pos
                    h = self.heuristic(neighbor, goal)
                    f = tentative_g + h
                    counter += 1
                    heapq.heappush(frontier, (f, counter, tentative_g, neighbor))

        return self.no_path_result()
