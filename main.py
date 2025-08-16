"""
Benchmarking harness for traversal costing algorithms.

Generates random traversals and path costs, runs both the baseline and optimized
implementations, and prints simple timing comparisons.
"""
from __future__ import annotations

import random
import copy
import logging
from statistics import mean, median, stdev
from typing import Dict, List, Tuple

from helpers import profile_call
from funcs import logic_as_is, improved_logic
from models import Traversal, Node, CostAtNode

logger = logging.getLogger("trackbase.main")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

# (traversals_n, nodesPerTraversal_n, pathCosts_n)
PARAM_SETS: List[Tuple[int, int, int]] = [
    (250, 150, 250),
    (500, 150, 250),
    (1000, 150, 250),
    (2000, 150, 250),
]


def make_random_data(
    seed: int,
    traversals_n: int,
    nodesPerTraversal_n: int,
    pathCosts_n: int,
) -> Tuple[List[Traversal], List[CostAtNode]]:
    """Create randomized inputs for a single benchmark run."""
    # Check if all parameter are greater than 1
    if traversals_n < 1 or nodesPerTraversal_n < 1 or pathCosts_n < 1:
        raise ValueError("All sizes must be >= 1")

    rnd = random.Random(seed)

    # Build traversals with node ids in [0, N-1] range.
    traversals = [
        Traversal(nodes=[Node(id=i) for i in range(nodesPerTraversal_n)])
        for _ in range(traversals_n)
    ]

    # randint upper bound must be N-1 to avoid referencing non-existent nodes.
    path_costs = [
        CostAtNode(node_id=rnd.randint(
            0, nodesPerTraversal_n - 1), cost=rnd.randint(0, 9))
        for _ in range(pathCosts_n)
    ]
    return traversals, path_costs


def run_profiling(
    traversals: List[Traversal],
    path_costs: List[CostAtNode],
    n: int,
) -> Dict[str, Dict[str, List]]:
    """Run both algorithms and return timings and results."""
    result_sets = {
        "improved": {"durations": [], "results": [], "func": improved_logic},
        "asIs": {"durations": [], "results": [], "func": logic_as_is},
    }

    # Running both functions for 'n' number of times.
    for i in range(n):
        logger.debug("Profiling iteration %d/%d", i+1, n)
        for name, data in result_sets.items():
            try:
                outcome = profile_call(
                    data["func"], [copy.deepcopy(
                        traversals), copy.deepcopy(path_costs)]
                )
                results, duration = outcome[0], outcome[1]
                data["results"].append([t.total_cost for t in results])
                data["durations"].append(duration)
            except Exception:
                logger.exception("Error while profiling function '%s'", name)
                raise

    return result_sets


def compute_results(
    param_sets: List[Tuple[int, int, int]],
    seed: int = 42,
    repeats: int = 5,
) -> Dict[Tuple[int, int, int], Dict[str, Dict[str, List]]]:
    """Run all parameter sets; return a mapping from case -> result_sets."""
    all_results = {}
    for case in param_sets:
        traversals_n, nodesPerTraversal_n, pathCosts_n = case
        logger.info(
            f"Case: Traversals={traversals_n}, Nodes/Traversal={nodesPerTraversal_n}, PathCosts={pathCosts_n}"
        )
        traversals, path_costs = make_random_data(
            seed=seed,
            traversals_n=traversals_n,
            nodesPerTraversal_n=nodesPerTraversal_n,
            pathCosts_n=pathCosts_n,
        )
        all_results[case] = run_profiling(traversals, path_costs, repeats)
    return all_results


def display_stats(all_results) -> None:
    for case, result_sets in all_results.items():
        traversals_n, nodesPerTraversal_n, pathCosts_n = case
        print(
            f"\n=== Results for Traversals={traversals_n}, Nodes/Traversal={nodesPerTraversal_n}, PathCosts={pathCosts_n} ==="
        )

        agg = {}
        for key, data in result_sets.items():
            duration = data["durations"]
            agg[key] = mean(duration)

            print(
                f"\t{key:>8}: mean={mean(duration):.2f} ms | median={median(duration):.2f} ms | stdev={stdev(duration):.2f} ms | samples={len(duration)}"
            )

        faster = min(agg, key=agg.get)
        slower = max(agg, key=agg.get)
        speedup = agg[slower] / agg[faster]
        print(
            f"\t→ On Average {faster} function is {speedup:.2f}× faster than {slower} function")


def sanity_check(all_results) -> None:
    for case, result_sets in all_results.items():
        # Sanity Check
        if result_sets["asIs"]["results"] != result_sets["improved"]["results"]:
            print("\t(!) Algorithms don't return the same output. (!)")
        else:
            print("\t(!) Both the Algorithms return same output.(!)")

        print("")


def print_results(param_sets: List[Tuple[int, int, int]]) -> None:
    all_results = compute_results(param_sets)
    sanity_check(all_results=all_results)
    display_stats(all_results=all_results)


if __name__ == "__main__":
    logger.info("Traversal Costing Benchmark starting....")
    try:
        print_results(PARAM_SETS)
    except Exception:
        logger.exception("Benchmark run failed")
        raise
    finally:
        logger.info("Traversal Costing Benchmark finished.")
