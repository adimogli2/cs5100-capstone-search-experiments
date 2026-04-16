"""
Breadth-First Search (BFS)
==========================
BFS explores nodes level by level, expanding all neighbors at depth d
before any node at depth d+1.

Data structure : FIFO queue (collections.deque)
Completeness   : Complete — will always find a solution if one exists
                 (on finite graphs).
Optimality     : Optimal for uniform-cost graphs (all step costs equal),
                 because it always expands the shallowest node first.
                 NOT optimal when step costs differ (use UCS instead).
Time complexity : O(b^d) where b = branching factor, d = solution depth.
Space complexity: O(b^d) — must store all frontier nodes at the current depth.
"""

from collections import deque

from algorithms.base import SearchAlgorithm, SearchResult


class BFS(SearchAlgorithm):
    """Breadth-First Search — uninformed, complete, optimal on uniform costs."""

    def search(self) -> SearchResult:
        """
        Implementation guide (fill this in when ready):

        1. Initialise a deque frontier with the start node.
           Each frontier entry should be just the position (row, col).

        2. Initialise an explored set containing the start position
           (mark on enqueue, not on expansion, to avoid redundant entries).

        3. Initialise a came_from dict: {start: None}.

        4. Pop from the LEFT of the deque (FIFO order).
           Increment nodes_expanded each time you pop.

        5. If the popped node is the goal:
           - Call self.reconstruct_path(came_from, goal) to get the path.
           - Compute path_cost as (len(path) - 1) * 1.0  (uniform cost = 1).
           - Return SearchResult(path, path_cost, nodes_expanded, success=True).

        6. For each neighbor from self.grid.get_neighbors(pos):
           - Skip if already in explored.
           - Mark explored, record came_from[neighbor] = pos.
           - Append to the RIGHT of the deque.

        7. If the frontier empties without finding the goal,
           return self.no_path_result().
        """
        start = self.grid.start
        goal  = self.grid.goal

        frontier   = deque([start])
        explored   = {start}
        came_from  = {start: None}
        nodes_expanded = 0

        while frontier:
            pos = frontier.popleft()
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
                    explored.add(neighbor)
                    came_from[neighbor] = pos
                    frontier.append(neighbor)

        return self.no_path_result()
