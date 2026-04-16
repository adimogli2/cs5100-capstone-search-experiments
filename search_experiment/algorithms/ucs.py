"""
Uniform-Cost Search (UCS)
=========================
UCS expands the node with the lowest cumulative path cost g(n) first,
making it the informed generalisation of BFS for weighted graphs.

Data structure : Min-heap priority queue ordered by g(n) (heapq)
Completeness   : Complete — finds a solution whenever one exists,
                 provided all step costs are positive.
Optimality     : Optimal — always finds the least-cost path when step
                 costs are non-negative.  Equivalent to Dijkstra's
                 algorithm when all edge weights are non-negative.
Time complexity : O(b^(1 + floor(C*/ε))) where C* = optimal cost,
                 ε = minimum step cost.
Space complexity: O(b^(1 + floor(C*/ε))) — same as time in the worst case.

Note: for this experiment all step costs are 1.0, so UCS and BFS will
expand nodes in the same order and produce identical results.
"""

import heapq

from algorithms.base import SearchAlgorithm, SearchResult


class UCS(SearchAlgorithm):
    """Uniform-Cost Search — uninformed, complete, optimal for non-negative costs."""

    def search(self) -> SearchResult:
        """
        Implementation guide (fill this in when ready):

        1. Initialise a min-heap frontier as a list.
           Push (g=0.0, start) using heapq.heappush.
           Use a counter to break ties if needed:
             heapq.heappush(frontier, (g, counter, pos))

        2. Initialise a cost_so_far dict: {start: 0.0}.

        3. Initialise a came_from dict: {start: None}.

        4. Pop the lowest-cost entry with heapq.heappop.
           Increment nodes_expanded.
           If the popped cost is greater than cost_so_far[pos], skip
           (stale entry — a cheaper path was already found).

        5. If the popped node is the goal:
           - Call self.reconstruct_path(came_from, goal).
           - Return SearchResult(path, cost_so_far[goal],
                                 nodes_expanded, success=True).

        6. For each neighbor from self.grid.get_neighbors(pos):
           - new_cost = cost_so_far[pos] + self.grid.step_cost(pos, neighbor)
           - If neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
               Update cost_so_far[neighbor] = new_cost.
               Record came_from[neighbor] = pos.
               Push (new_cost, counter, neighbor) onto the heap.

        7. If the heap empties without finding the goal,
           return self.no_path_result().
        """
        start = self.grid.start
        goal  = self.grid.goal

        counter      = 0
        cost_so_far  = {start: 0.0}
        came_from    = {start: None}
        frontier     = [(0.0, counter, start)]
        nodes_expanded = 0

        while frontier:
            g, _, pos = heapq.heappop(frontier)

            if g > cost_so_far[pos]:
                continue

            nodes_expanded += 1

            if pos == goal:
                path = self.reconstruct_path(came_from, pos)
                return SearchResult(
                    path=path,
                    path_cost=cost_so_far[goal],
                    nodes_expanded=nodes_expanded,
                    success=True,
                )

            for neighbor in self.grid.get_neighbors(pos):
                new_cost = cost_so_far[pos] + self.grid.step_cost(pos, neighbor)

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor]   = pos
                    counter += 1
                    heapq.heappush(frontier, (new_cost, counter, neighbor))

        return self.no_path_result()
