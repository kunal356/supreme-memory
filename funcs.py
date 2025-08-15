"""Core algorithms for computing traversal costs.

The module contains two implementations:
- logic_as_is: the original, baseline algorithm (intentionally naive / O(T×P×N)).
- improved_logic: optimized algorithm that indexes costs by node_id to reduce complexity.
"""
from collections import defaultdict
from typing import Dict, List
from models import Traversal, CostAtNode


def logic_as_is(traversals: List[Traversal], pathCosts: List[CostAtNode]) -> List[Traversal]:
    """Baseline traversal costing algorithm (kept for parity/testing).

    For each traversal:
      1) Clear each node's `costs`.
      2) For every cost in `pathCosts`, scan all nodes and append the cost to the node
         whose id matches `cost.node_id` (nested loop).
      3) Sum all costs attached to nodes into `traversal.total_cost`.

    Time complexity:
        O(T × (N + P×N + N×K)) ≈ O(T × P × N), where
          T = # of traversals, N = # of nodes/traversal, P = # of pathCosts,
          K = avg # of costs per node (usually small, but the P×N dominates).

    Args:
        traversals: Traversals to augment with per-node costs and total_cost.
        pathCosts: Flat list of costs, each tagged with a node_id.
    Returns:
        The same list of traversals, updated in-place (also returned for convenience).
    """
    for traversal in traversals:
        # Clear/initialize costs per node
        for node in traversal.nodes:
            node.costs = []

        # For each cost, linearly scan nodes in this traversal looking for a match
        for cost in pathCosts:
            for node in traversal.nodes:
                if node.id == cost.node_id:
                    node.costs.append(cost)

        # Accumulate total_cost
        for node in traversal.nodes:
            if node.costs:
                for cost in node.costs:
                    traversal.total_cost += cost.cost

    return traversals


def improved_logic(traversals: List[Traversal], pathCosts: List[CostAtNode]) -> List[Traversal]:
    """Optimized traversal costing algorithm using a cost index (O(P + T×N)).

    Strategy:
      - Build an index `by_node` that groups costs by their `node_id` once (O(P)).
      - For each traversal, walk its nodes exactly once; attach the pre-indexed list
        from `by_node` and accumulate totals (O(T×N)).

    Benefits:
      - Avoids re-scanning `pathCosts` per traversal (no O(T×P×N) nested loops).
      - Low memory overhead by reusing the same lists from the index.

    Args:
        traversals: Traversals to augment with per-node costs and total_cost.
        pathCosts: Flat list of costs, each tagged with a node_id.

    Returns:
        The same list of traversals, updated in-place (also returned for convenience).
    """
    # Group costs by node_id for O(1) lookup per node
    cost_by_node: Dict[int, List[CostAtNode]] = defaultdict(list)
    sum_by_node = defaultdict(int) # Hash Map of Nodeid and Cost
    for c in pathCosts:
        cost_by_node[c.node_id].append(c)
        sum_by_node[c.node_id] += c.cost 

    # Attach and sum per traversal
    for traversal in traversals:
        traversal.total_cost = 0  # reset/initialize per traversal
        for node in traversal.nodes:
            # Point to the shared list from the index (avoid per-node copying)
            node.costs = cost_by_node.get(node.id, [])
            if node.costs:
                traversal.total_cost += sum_by_node.get(node.id, 0)

    return traversals
