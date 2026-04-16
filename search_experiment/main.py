"""
main.py — entry point for the CS5100 search algorithm experiment.

Usage examples
--------------
python main.py                              # full experiment, both modes
python main.py --mode fixed                 # fixed seeds only
python main.py --size 10                    # 10x10 grids only
python main.py --size 10 --mode fixed       # quick smoke-run (all stubs)
python main.py --algorithm AStar            # one algorithm across all sizes/modes
python main.py --output results/my_run.csv  # custom output path
"""

import argparse
import datetime
import time

from experiment.runner import ALGORITHM_REGISTRY, SIZES, ExperimentRunner


def parse_args() -> argparse.Namespace:
    valid_algo_names = sorted({cls.__name__ for cls, _ in ALGORITHM_REGISTRY})

    parser = argparse.ArgumentParser(
        description="CS5100 Search Algorithm Experiment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--size",
        type=int,
        choices=SIZES,
        default=None,
        metavar="{10,25,100}",
        help="Filter to a single grid size (default: all sizes)",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        choices=valid_algo_names,
        default=None,
        metavar=f"{{{','.join(valid_algo_names)}}}",
        help="Filter to a single algorithm (default: all algorithms)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["fixed", "random", "both"],
        default="both",
        help="Seed mode: fixed seeds, random seeds, or both (default: both)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/results.csv",
        help="Path for the output CSV file (default: results/results.csv)",
    )
    return parser.parse_args()


def print_header(args: argparse.Namespace) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sizes_label = f"{args.size}x{args.size}" if args.size else "10x10, 25x25, 100x100"
    algo_label  = args.algorithm if args.algorithm else "all"

    print("=" * 70)
    print("  CS5100 Search Algorithm Experiment")
    print("=" * 70)
    print(f"  Timestamp : {timestamp}")
    print(f"  Grid sizes: {sizes_label}")
    print(f"  Algorithm : {algo_label}")
    print(f"  Mode      : {args.mode}")
    print(f"  Output    : {args.output}")
    print("=" * 70)
    print()


def print_summary(summary: dict, output_path: str) -> None:
    print()
    print("=" * 70)
    print("  Experiment Summary")
    print("=" * 70)
    print(f"  Total runs attempted : {summary['total_runs']}")
    print(f"  Completed (success)  : {summary['completed']}")
    print(f"  Skipped (stub / err) : {summary['skipped']}")
    print(f"  Errors               : {summary['errors']}")
    print(f"  Total wall time      : {summary['total_time_seconds']:.3f}s")
    print(f"  Output file          : {output_path}")
    print("=" * 70)
    if summary["skipped"] > 0:
        print()
        print("  NOTE: Skipped algorithms need implementation in algorithms/")
        print("        See README.md for guidance.")
    print()


def main() -> None:
    args = parse_args()
    print_header(args)

    runner = ExperimentRunner(output_path=args.output)

    sizes      = [args.size] if args.size else None
    algorithms = [args.algorithm] if args.algorithm else None

    summary = runner.run_all(sizes=sizes, algorithms=algorithms, mode=args.mode)
    print_summary(summary, args.output)


if __name__ == "__main__":
    main()
