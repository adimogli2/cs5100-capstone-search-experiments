"""
ExperimentRunner — orchestrates all grid generation, algorithm execution,
metric collection, and CSV output for the search experiment.
"""

import csv
import os
import time

from algorithms.astar import AStar
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.greedy import GreedyBestFirst
from algorithms.ucs import UCS
from environment.grid import Grid
from heuristics.heuristics import HEURISTICS
from metrics.recorder import MetricsRecorder, MetricsResult

SIZES: list[int] = [10, 25, 100]

FIXED_SEEDS: list[int] = [42, 123, 456, 789, 1337, 2024, 3141, 8675, 9999, 1111]

RUNS_PER_CONFIG: int = 10

ALGORITHM_REGISTRY: list[tuple] = [
    (BFS, None),
    (DFS, None),
    (UCS, None),
    (GreedyBestFirst, "manhattan"),
    (GreedyBestFirst, "euclidean"),
    (AStar, "manhattan"),
    (AStar, "euclidean"),
    (AStar, "zero"),
    (AStar, "inadmissible"),
]

CSV_HEADER: list[str] = [
    "run_id",
    "mode",
    "algorithm",
    "heuristic",
    "grid_size",
    "grid_seed",
    "obstacle_density",
    "nodes_expanded",
    "runtime_ms",
    "path_cost",
    "path_length",
    "success",
]

class ExperimentRunner:
    # runs the experiment
    def __init__(self, output_path: str = "results/results.csv"):
        self.output_path = output_path
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if not os.path.exists(output_path):
            with open(output_path, "w", newline="") as f:
                csv.writer(f).writerow(CSV_HEADER)

        self.recorder = MetricsRecorder()

    def run_all(self, sizes: list[int] | None = None, algorithms: list[str] | None = None, mode: str = "both") -> dict:
        active_sizes = sizes if sizes is not None else SIZES
        active_registry = [
            (cls, h) for cls, h in ALGORITHM_REGISTRY
            if algorithms is None or cls.__name__ in algorithms
        ]
        modes = _resolve_modes(mode)

        total_runs = 0
        completed = 0
        skipped = 0
        errors = 0
        wall_start = time.perf_counter()

        for size in active_sizes:
            for run_mode in modes:
                seeds = FIXED_SEEDS if run_mode == "fixed" else [None] * RUNS_PER_CONFIG

                for seed in seeds:
                    # Generate one grid, shared across all algorithms on this run
                    grid = Grid(size=size, seed=seed)

                    for algo_cls, heuristic_key in active_registry:
                        heuristic_fn = HEURISTICS[heuristic_key] if heuristic_key else None

                        if heuristic_fn is not None:
                            algo = algo_cls(grid, heuristic=heuristic_fn)
                        else:
                            algo = algo_cls(grid)

                        metrics = self.recorder.wrap_search(algo, grid, mode=run_mode)
                        self._append_to_csv(metrics)
                        _print_progress(metrics)

                        total_runs += 1
                        if metrics.success:
                            completed += 1
                        elif metrics.nodes_expanded == 0 and not metrics.success:
                            skipped += 1
                        else:
                            errors += 1

        total_time = time.perf_counter() - wall_start

        return {
            "total_runs": total_runs,
            "completed": completed,
            "skipped": skipped,
            "errors": errors,
            "total_time_seconds":  round(total_time, 3),
        }

    def _append_to_csv(self, result: MetricsResult) -> None:
        with open(self.output_path, "a", newline="") as f:
            csv.writer(f).writerow(result.to_csv_row())

def _resolve_modes(mode: str) -> list[str]:
    if mode == "both":
        return ["fixed", "random"]
    return [mode]

def _print_progress(m: MetricsResult) -> None:
    status = "OK  " if m.success else "SKIP"
    print(
        f"  [{m.algorithm:<16}] [{m.heuristic:<12}] | "
        f"{m.grid_size:>3}x{m.grid_size:<3} | "
        f"seed={m.grid_seed:<10} | "
        f"nodes={m.nodes_expanded:>6} | "
        f"{m.runtime_ms:>8.2f}ms | "
        f"cost={m.path_cost:>6.1f} | "
        f"{status}"
    )
