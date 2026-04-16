from collections import deque

from algorithms.base import SearchAlgorithm, SearchResult


class BFS(SearchAlgorithm):
    """Breadth-first search for uniform-cost grids."""

    def search(self) -> SearchResult:
        start = self.grid.start
        goal = self.grid.goal

        # queue of nodes to visit
        frontier = deque([start])

        # mark visited on enqueue
        explored = {start}

        # parent map for path rebuild
        came_from = {start: None}

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