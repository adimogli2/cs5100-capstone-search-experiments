import heapq

from algorithms.base import SearchAlgorithm, SearchResult


class UCS(SearchAlgorithm):
    """Uniform-cost search using path cost g(n)."""

    def search(self) -> SearchResult:
        start = self.grid.start
        goal = self.grid.goal

        counter = 0
        cost_so_far = {start: 0.0}
        came_from = {start: None}

        # heap entry: (g, tie, pos)
        frontier = [(0.0, counter, start)]

        nodes_expanded = 0

        while frontier:
            g, _, pos = heapq.heappop(frontier)

            # skip outdated entry
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
                    came_from[neighbor] = pos
                    counter += 1
                    heapq.heappush(frontier, (new_cost, counter, neighbor))

        return self.no_path_result()