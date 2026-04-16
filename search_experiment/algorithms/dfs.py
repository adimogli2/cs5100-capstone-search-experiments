from algorithms.base import SearchAlgorithm, SearchResult


class DFS(SearchAlgorithm):
    """Depth-first search on a finite grid."""

    def search(self) -> SearchResult:
        start = self.grid.start
        goal = self.grid.goal

        # stack for DFS
        stack = [start]

        # mark visited on pop
        explored = set()

        # parent map for path rebuild
        came_from = {start: None}

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