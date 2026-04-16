"""
Depth-First Search (DFS)
========================
DFS explores as deep as possible along each branch before backtracking.

Data structure : LIFO stack (Python list used as stack via .append/.pop)
Completeness   : NOT complete on infinite or very deep graphs — can get
                 trapped in infinite loops without cycle detection.
                 Complete on finite graphs with explored-set tracking.
Optimality     : NOT optimal — finds the first path, not the shortest.
                 The solution found depends on neighbour ordering.
Time complexity : O(b^m) where b = branching factor, m = max depth.
                 Can be much worse than BFS if solution is shallow.
Space complexity: O(b*m) — only stores nodes on the current path and their
                 siblings; much lower memory than BFS in practice.
"""

from algorithms.base import SearchAlgorithm, SearchResult


class DFS(SearchAlgorithm):
    """Depth-First Search — uninformed, complete on finite graphs, not optimal."""

    def search(self) -> SearchResult:
        """
        Implementation guide (fill this in when ready):

        1. Initialise a list stack with the start node.
           Each entry should be just the position (row, col).

        2. Initialise an explored set (empty at start — mark on pop,
           not on push, so re-pushed nodes are properly revisited
           if an earlier branch put them on the stack first).

        3. Initialise a came_from dict: {start: None}.

        4. Pop from the END of the list (LIFO order).
           Skip if already in explored, then mark explored.
           Increment nodes_expanded each time a node is processed.

        5. If the popped node is the goal:
           - Call self.reconstruct_path(came_from, goal).
           - Compute path_cost as (len(path) - 1) * 1.0.
           - Return SearchResult(path, path_cost, nodes_expanded, success=True).

        6. For each neighbor from self.grid.get_neighbors(pos):
           - Skip if already in explored.
           - Record came_from[neighbor] = pos  (only if not yet set,
             to preserve the first path found to each node).
           - Push onto the stack.

        7. If the stack empties without finding the goal,
           return self.no_path_result().
        """
        start = self.grid.start
        goal  = self.grid.goal

        stack      = [start]
        explored   = set()
        came_from  = {start: None}
        nodes_expanded = 0

        while stack:
            pos = stack.pop()

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
                    stack.append(neighbor)

        return self.no_path_result()
