import heapq

from algorithms.base import SearchAlgorithm, SearchResult
from heuristics.heuristics import manhattan_distance


class GreedyBestFirst(SearchAlgorithm):
    """Greedy best-first search using h(n) only."""

    def __init__(self, grid, heuristic=None):
        if heuristic is None:
            heuristic = manhattan_distance
        super().__init__(grid, heuristic)

    def search(self) -> SearchResult:
        start = self.grid.start
        goal = self.grid.goal

        counter = 0
        explored = set()
        came_from = {start: None}

        # heap entry: (h, tie, pos)
        frontier = [(self.heuristic(start, goal), counter, start)]

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