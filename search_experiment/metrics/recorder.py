"""
Metrics collection for search algorithm experiments.

MetricsResult  — dataclass holding every field written to results.csv
MetricsRecorder — wraps a search() call measuring runtime, and building a MetricsResult
"""

import logging
import time
from dataclasses import dataclass

from heuristics.heuristics import HEURISTICS

logger = logging.getLogger(__name__)

@dataclass
class MetricsResult:
    # all data captured for a single run
    run_id: int
    mode: str # "fixed" or "random"
    algorithm: str # e.g. "AStar"
    heuristic: str
    grid_size: int # e.g. 10 for a 10x10 grid
    grid_seed: int
    obstacle_density: float
    nodes_expanded: int
    runtime_ms: float
    path_cost: float
    path_length: int # number of steps (= len(path) - 1, or 0 on failure)
    success: bool

    def to_csv_row(self) -> list:
        # return all fields as a list, matches CSV schema
        return [
            self.run_id,
            self.mode,
            self.algorithm,
            self.heuristic,
            self.grid_size,
            self.grid_seed,
            self.obstacle_density,
            self.nodes_expanded,
            self.runtime_ms,
            self.path_cost,
            self.path_length,
            self.success,
        ]


class MetricsRecorder:
    def __init__(self):
        self.run_counter: int = 0

    def wrap_search(self, algorithm, grid, mode: str) -> MetricsResult:
        # run an algorithm on a grid and return a MetricsResult
        # measures runtime and records metadata (algorithm/heuristic/mode/grid)
        self.run_counter += 1

        # meta data
        algo_name = type(algorithm).__name__

        heuristic_fn = algorithm.heuristic
        if heuristic_fn is None:
            heuristic_name = "none"
        else:
            heuristic_name = heuristic_fn.__name__

        # run search
        skipped = False
        # perf_counter to track runtime, chosen for its accuracy on short durations 
        start = time.perf_counter()

        try:
            result = algorithm.search()
        except Exception as exc:
            logger.error(
                "Unexpected error in %s.search(): %s: %s",
                algo_name, type(exc).__name__, exc,
            )
            result = algorithm.no_path_result()
            skipped = True

        elapsed_ms = (time.perf_counter() - start) * 1000.0
        
        if skipped:
            nodes_expanded = 0
            runtime_ms = 0.0
            path_cost = 0.0
            path_length = 0
            success = False
        else:
            nodes_expanded = result.nodes_expanded
            runtime_ms = round(elapsed_ms, 4)
            path_cost = result.path_cost
            path_length = max(len(result.path) - 1, 0)
            success = result.success

        return MetricsResult(
            run_id = self.run_counter,
            mode = mode,
            algorithm = algo_name,
            heuristic = heuristic_name,
            grid_size = grid.size,
            grid_seed = grid.seed,
            obstacle_density = round(grid.obstacle_density, 4),
            nodes_expanded = nodes_expanded,
            runtime_ms = runtime_ms,
            path_cost = path_cost,
            path_length = path_length,
            success = success
        )
