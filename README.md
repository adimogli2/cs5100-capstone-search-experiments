# cs5100-capstone-search-experiments

CS5100 capstone project reproducing Hart, Nilsson & Raphael (1968) — comparing A* against uninformed and greedy search on grid-based pathfinding across three grid sizes and nine algorithm/heuristic combinations.

## Usage

Run from the repo root:

```bash
cd search_experiment
python3 main.py
```

This runs the full experiment:
- **Grid sizes**: 10×10, 25×25, 100×100
- **Modes**: fixed seeds and random seeds
- **Algorithms**: BFS, DFS, UCS, Greedy Best-First (Manhattan/Euclidean), A* (Manhattan/Euclidean/Zero/Inadmissible)
- **Output**: appends results to `results/results.csv` (creates it with a header if missing)

## Flags

Run from `search_experiment/`:

- **`--size {10,25,100}`**: run only one grid size (default: all)
- **`--algorithm {BFS,DFS,UCS,GreedyBestFirst,AStar}`**: run only one algorithm (default: all)
- **`--mode {fixed,random,both}`**: choose fixed seeds, random seeds, or both (default: both)
- **`--output <path>`**: CSV output path (default: `results/results.csv`)

Examples:

```bash
python3 main.py --mode fixed
python3 main.py --size 10 --algorithm AStar
python3 main.py --output results/my_run.csv
```