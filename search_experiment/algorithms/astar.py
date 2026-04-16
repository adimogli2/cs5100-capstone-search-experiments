import heapq

from algorithms.base import SearchAlgorithm, SearchResult
from heuristics.heuristics import manhattan_distance


class AStar(SearchAlgorithm):
    """A* search using f(n) = g(n) + h(n)."""

    def __init__(self, grid, heuristic=None):
        if heuristic is None:
            heuristic = manhattan_distance
        super().__init__(grid, heuristic)

    def search(self) -> SearchResult:
        start = self.grid.start
        goal = self.grid.goal

        # best known cost to each node
        g_score: dict[tuple, float] = {start: 0.0}

        # parent map for path rebuild
        came_from: dict[tuple, tuple | None] = {start: None}

        # heap entry: (f, tie, g, pos)
        counter = 0
        h_start = self.heuristic(start, goal)
        frontier = [(h_start, counter, 0.0, start)]

        nodes_expanded = 0

        while frontier:
            f, _, g, pos = heapq.heappop(frontier)

            # skip outdated entry
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

                # found a better path
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    came_from[neighbor] = pos

                    h = self.heuristic(neighbor, goal)
                    f = tentative_g + h
                    counter += 1
                    heapq.heappush(frontier, (f, counter, tentative_g, neighbor))

        return self.no_path_result()