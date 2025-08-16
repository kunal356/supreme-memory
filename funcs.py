"""Core algorithms for computing traversal costs.

The module contains two implementations:
- logic_as_is: The original algorithm.
- improved_logic: Optimized algorithm that indexes costs by node_id to reduce complexity.
"""
from collections import defaultdict
from typing import Dict, List, Optional
import logging

from models import Traversal, CostAtNode

logger = logging.getLogger("trackbase.funcs")


def _ensure_lists(traversals: Optional[List[Traversal]], pathCosts: Optional[List[CostAtNode]]):
    if traversals is None or pathCosts is None:
        logger.warning("Received Empty/None input(s): traversals=%s pathCosts=%s",
                       traversals is None, pathCosts is None)
        return traversals or [], pathCosts or []
    return traversals, pathCosts


def logic_as_is(traversals: List[Traversal], pathCosts: List[CostAtNode]) -> List[Traversal]:
    """Original traversal costing algorithm.
    Args:
        traversals: Traversals to augment with per-node costs and total_cost.
        pathCosts: Flat list of costs, each tagged with a node_id.
    Returns:
        The same list of traversals, updated in-place.
    """
    traversals, pathCosts = _ensure_lists(
        traversals=traversals, pathCosts=pathCosts)
    logger.debug("logic_as_is: START (traversals=%d, costs=%d)",
                 len(traversals), len(pathCosts))

    for traversal in traversals:
        # Clear/initialize costs per node
        for node in traversal.nodes:
            node.costs = []

        # For each cost, linearly scan nodes in this traversal looking for a match
        for cost in pathCosts:
            for node in traversal.nodes:
                if node.id == cost.node_id:
                    node.costs.append(cost)

        # Computes the total cost of traversal by adding the costs of each node in the path.
        for node in traversal.nodes:
            if node.costs:
                for cost in node.costs:
                    traversal.total_cost += cost.cost
    logger.debug("logic_as_is: END")
    return traversals


def improved_logic(traversals: List[Traversal], pathCosts: List[CostAtNode]) -> List[Traversal]:
    """Optimized traversal costing algorithm using a cost index.
    Args:
        traversals: Traversals to augment with per-node costs and total_cost.
        pathCosts: Flat list of costs, each tagged with a node_id.

    Returns:
        The same list of traversals, updated in-place (also returned for convenience).
    """

    traversals, pathCosts = _ensure_lists(
        traversals=traversals, pathCosts=pathCosts)
    logger.debug("improved_logic: START (traversals=%d, costs=%d)",
                 len(traversals), len(pathCosts))

    # Group costs by node_id for O(1) lookup per node (cost_by_node).
    # Create index/hashmap of cost and node_id (sum_by_node).
    cost_by_node: Dict[int, List[CostAtNode]] = defaultdict(list)
    sum_by_node = defaultdict(int)
    for c in pathCosts:
        if c.node_id < 0:
            logger.warning("Node with negative node_id found: %s", c)
            continue
        cost_by_node[c.node_id].append(c)
        sum_by_node[c.node_id] += c.cost

    # Compute Total cost for traversals using indexes
    for traversal in traversals:
        traversal.total_cost = 0  # Reset/Initialize total_cost per traversal
        for node in traversal.nodes:
            # Point to the shared list of costs from the index (avoid per-node copying)
            node.costs = cost_by_node.get(node.id, [])
            if node.costs:
                # Calculate total cost for entire traversal
                traversal.total_cost += sum_by_node.get(node.id, 0)
    logger.debug("improved_logic: END")
    return traversals
